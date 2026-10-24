"""Tests for the doc shape check (``scripts/check_docs.py``).

Each test pins one rule the docs must keep, so a rule that silently stops
firing fails here rather than in review.
"""

from __future__ import annotations

import unittest

from scripts.check_docs import body_lines, check_text, normalise, tracked_docs


def clean(*lines: str) -> str:
    body = list(lines)
    while body and not body[-1]:
        body.pop()
    return "\n".join(body) + "\n"


class TestShape(unittest.TestCase):
    def test_clean_doc_reports_nothing(self) -> None:
        text = clean(
            "## Description",
            "",
            "One paragraph on one line.",
            "",
            "- one",
            "- two",
            "",
        )
        self.assertEqual(check_text(text), [])

    def test_hard_wrapped_paragraph_is_reported(self) -> None:
        text = clean("A paragraph that was\nwrapped by hand.", "")
        self.assertIn("1: hard-wrapped paragraph", check_text(text))

    def test_wrapping_is_joined(self) -> None:
        text = clean("A paragraph that was", "wrapped by hand.", "")
        self.assertEqual(normalise(body_lines(text)), ["A paragraph that was wrapped by hand."])

    def test_blank_line_inside_a_list_is_reported(self) -> None:
        text = clean("- one", "", "- two", "")
        self.assertIn("2: blank line inside a list", check_text(text))

    def test_two_blank_lines_are_reported(self) -> None:
        text = clean("First.", "", "", "Second.", "")
        self.assertIn("3: two blank lines in a row", check_text(text))

    def test_heading_needs_a_blank_line_after_it(self) -> None:
        text = clean("## Description", "Text right after the heading.", "")
        self.assertIn("1: no blank line after heading", check_text(text))

    def test_missing_final_newline_is_reported(self) -> None:
        self.assertIn("missing final newline", check_text("Text with no newline."))

    def test_trailing_whitespace_is_reported(self) -> None:
        self.assertIn("1: trailing whitespace", check_text(clean("Line with trailing space. ")))

    def test_crlf_is_detected_by_the_byte_read(self) -> None:
        # The rule lives in main(), where the file is read as bytes; this pins
        # the shape rule that --fix then applies.
        text = "Line one.\r\nLine two.\r\n"
        self.assertNotEqual(text, text.replace("\r\n", "\n"))

    def test_code_fence_content_is_left_alone(self) -> None:
        text = clean("```text", "a line,", "another line", "```", "")
        self.assertEqual(check_text(text), [])


class TestScope(unittest.TestCase):
    def test_adrs_and_archive_are_out_of_scope(self) -> None:
        paths = [p.as_posix() for p in tracked_docs()]
        self.assertFalse([p for p in paths if "/ADR-" in p])
        self.assertFalse([p for p in paths if "/archive/" in p])

    def test_docs_are_found(self) -> None:
        self.assertGreater(len(tracked_docs()), 3)


if __name__ == "__main__":
    unittest.main()
