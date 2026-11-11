"""`textwerk list` with the group's plug-ins (docs/cli.md)."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import textwerk as tw


class ListTest(tw.ToolTestCase):

    def lines(self):
        result = tw.run("list")
        self.assertExit(result, 0)
        return [line for line in result.stdout.splitlines() if line.strip()]

    def test_at_least_three_plugins(self):
        self.assertGreaterEqual(len(self.lines()), 3, "version 1 needs at least three plug-ins")

    def test_line_format(self):
        lines = self.lines()
        self.assertTrue(lines, "no plug-ins listed")
        for line in lines:
            parts = line.split("\t")
            self.assertEqual(len(parts), 2, f"expected <name><TAB><description>: {line!r}")
            self.assertRegex(parts[0], tw.NAME_RE)
            self.assertTrue(parts[1].strip(), f"empty description: {line!r}")

    def test_sorted_and_unique(self):
        names = [line.split("\t")[0] for line in self.lines()]
        self.assertTrue(names, "no plug-ins listed")
        self.assertEqual(names, sorted(set(names)))


if __name__ == "__main__":
    unittest.main()
