"""Tests for the public-boundary check (``scripts/leak_check.py``).

Path fixtures are the private Android repository's real inventory, so a rule
change that stops covering, say, ``libQnnHtp.so`` fails here.
"""

from __future__ import annotations

import contextlib
import io
import unittest

from scripts.leak_check import (
    REPO_ROOT,
    check,
    classify,
    gitlink_findings,
    main,
    scan,
    submodule_entries,
    submodule_sections,
)

#: Representative private-track paths, mapped to the rule that must catch them.
PRIVATE_PATHS = {
    "app/src/main/jniLibs/arm64-v8a/libQnnHtp.so": "native-library",
    "app/src/main/jniLibs/arm64-v8a/libQnnDspV66Stub.so": "native-library",
    "qnn/2.31.0/x86_64-windows-msvc/QnnHtp.dll": "native-library",
    "app/build.gradle.kts": "android-project",
    "build.gradle": "android-project",
    "settings.gradle": "android-project",
    "app/src/main/AndroidManifest.xml": "android-project",
    "gradlew": "android-project",
    "app/src/main/java/com/kavi/app/qnn/QnnModelLoader.kt": "app-source",
    "app/src/main/cpp/qnn_loader_jni.cpp": "app-source",
    "gradle/wrapper/gradle-wrapper.jar": "android-package",
    "release/kavi-arm64.apk": "android-package",
    "build/outputs/kavi.aar": "android-package",
    "models/whisper_encoder.dlc": "compiled-model",
    "models/opus_mt_ctx.qnn": "compiled-model",
    "models/encoder.tflite": "compiled-model",
    "models/pytorch_model.bin": "model-weights",
    "models/encoder_fp16.onnx": "model-weights",
    "models/weights.safetensors": "model-weights",
    "release/kavi-release.jks": "secret-material",
    "release/upload-keystore.p12": "secret-material",
    "deploy/id_rsa": "secret-material",
    ".kavi.env": "machine-local",
    "android/local.properties": "machine-local",
    "bench-results/run_results_android.json": "on-device-result",
    "runs/2026-10/run_results_android_v1.json": "on-device-result",
}

#: Paths that must stay publishable -- the false-positive guard.
PUBLIC_PATHS = (
    "README.md",
    "LICENSE",
    "NOTICE",
    ".gitignore",
    ".gitmodules",
    "docs/contest-info.md",
    "docs/specifications.md",
    "prototype",
    "prototype/README.md",
    "scripts/leak_check.py",
    "scripts/link_check.py",
    "tests/test_leak_check.py",
    "tests/test_link_check.py",
    "docs/reference/phase-4-qnn-plan.md",
    "bench/qnn/convert_to_qnn.sh",
    "archive/pipeline.py",
)


class TestClassify(unittest.TestCase):
    """Rule matching: private paths are caught, public ones are not."""

    def test_private_paths_are_caught(self) -> None:
        for path, rule_id in PRIVATE_PATHS.items():
            with self.subTest(path=path):
                rule = classify(path)
                self.assertIsNotNone(rule, f"{path} slipped through the boundary")
                self.assertEqual(rule.id, rule_id)

    def test_public_paths_are_allowed(self) -> None:
        for path in PUBLIC_PATHS:
            with self.subTest(path=path):
                self.assertIsNone(classify(path), f"{path} is publishable")

    def test_every_rule_is_reachable(self) -> None:
        """A rule that matches nothing is dead weight and should be deleted."""
        hit = {finding.rule for finding in scan(PRIVATE_PATHS)}
        self.assertEqual(hit, set(PRIVATE_PATHS.values()))

    def test_matching_is_case_insensitive(self) -> None:
        self.assertIsNotNone(classify("APP/src/main/AndroidManifest.xml"))
        self.assertIsNotNone(classify("Models/PyTorch_Model.BIN"))


class TestGitlinks(unittest.TestCase):
    """The split's structural invariant: no gitlink to the private repo."""

    def test_gitlink_is_reported(self) -> None:
        (finding,) = gitlink_findings(["160000 1a2b3c 0\tandroid"])
        self.assertEqual(finding.rule, "gitlink")
        self.assertEqual(finding.path, "android")

    def test_public_sibling_gitlink_is_allowed_when_listed(self) -> None:
        entries = ["160000 1a2b3c 0\tprototype", "160000 def456 0\tandroid"]
        found = gitlink_findings(entries, ["prototype"])
        self.assertEqual([finding.path for finding in found], ["android"])

    def test_ordinary_modes_are_ignored(self) -> None:
        entries = ["100644 abc 0\tREADME.md", "100755 def 0\trun.sh"]
        self.assertEqual(gitlink_findings(entries), [])

    def test_submodule_entries_are_parsed(self) -> None:
        text = (
            "# a comment\n"
            '[submodule "prototype"]\n'
            "\tpath = prototype\n"
            "\turl = git@github.com:TanKhoiTV/kavi-prototype.git\n"
        )
        self.assertEqual(submodule_entries(text), [('[submodule "prototype"]', "prototype")])

    def test_comment_only_gitmodules_declares_nothing(self) -> None:
        self.assertEqual(submodule_sections("# the app repo is not a submodule\n"), [])
        self.assertEqual(submodule_entries("# nothing here\n"), [])


class TestThisRepository(unittest.TestCase):
    """What CI enforces on the real tree."""

    def test_boundary_holds_with_the_public_submodule_allowed(self) -> None:
        paths, found = check(REPO_ROOT, ["prototype"])
        self.assertEqual(found, [], f"private-track files are tracked: {found}")
        self.assertIn("README.md", paths)

    def test_the_public_submodule_would_be_reported_without_the_flag(self) -> None:
        """Guard against the allow-list silently covering more than prototype."""
        _, found = check(REPO_ROOT)
        self.assertEqual(
            sorted(finding.rule for finding in found), ["gitlink", "gitmodules"]
        )
        self.assertEqual({finding.path for finding in found}, {"prototype"})


class TestMain(unittest.TestCase):
    """CLI behaviour: exit status, the flag, and console-safe output."""

    def run_main(self, argv: list[str]) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(argv)
        return code, out.getvalue()

    def test_repository_passes_with_the_allowed_gitlink(self) -> None:
        code, out = self.run_main(["--allow-gitlink", "prototype"])
        self.assertEqual(code, 0, out)
        self.assertIn("OK", out)
        self.assertTrue(out.isascii())

    def test_missing_flag_reports_the_submodule(self) -> None:
        code, out = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("gitlink", out)

    def test_explicit_private_path_fails(self) -> None:
        code, out = self.run_main(["app/src/main/jniLibs/arm64-v8a/libQnnHtp.so"])
        self.assertEqual(code, 1)
        self.assertIn("native-library", out)
        self.assertTrue(out.isascii())


if __name__ == "__main__":
    unittest.main()
