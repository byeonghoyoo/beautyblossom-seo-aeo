"""Verify that the planning repository matches the audited facts."""
from pathlib import Path
import csv
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def read_csv(relative: str):
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


class RepositoryTests(unittest.TestCase):
    def test_required_document_order(self):
        required = [
            "docs/01-PRD.md",
            "docs/02-TECH-STACK.md",
            "docs/03-ARCHITECTURE.md",
            "docs/04-WORKFLOW.md",
            "docs/05-CLAUDE-CODE-INSTRUCTIONS.md",
            "docs/06-REVIEW-LOG.md",
            "docs/PROJECT-MAP.md",
        ]
        self.assertTrue(all((ROOT / path).is_file() for path in required))

    def test_audit_counts(self):
        summary = read_json("audit/data/summary.json")
        pages = read_csv("audit/inventories/page-inventory.csv")
        titles = read_csv("audit/inventories/title-locations.csv")
        self.assertEqual(summary["requested_urls"], 530)
        self.assertEqual(summary["unique_internal_html_final_urls"], 479)
        self.assertEqual(summary["multiple_title_pages"], 77)
        self.assertEqual(summary["additional_title_elements"], 143)
        self.assertEqual(len(pages), 479)
        self.assertEqual(len(titles), 143)
        self.assertEqual({row["site"] for row in pages}, {"kr", "en", "jp", "cn", "tw"})

    def test_validated_404_targets(self):
        records = read_json("audit/data/validated-urls.json")
        failures = [row for row in records if row["requested"].endswith("/107")]
        self.assertEqual(len(failures), 3)
        self.assertTrue(all(row["status"] == 404 for row in failures))

    def test_javascript_result_is_described_as_syntax_only(self):
        result = read_json("audit/data/javascript-syntax-check.json")
        self.assertEqual(result["checked"], 1470)
        self.assertEqual(result["failures"], [])
        self.assertIn("no execution", result["mode"])

    def test_visual_workflows_exist(self):
        markdown = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md"))
        self.assertGreaterEqual(markdown.count("```mermaid"), 7)

    def test_relative_markdown_links_exist(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for document in ROOT.rglob("*.md"):
            for target in pattern.findall(document.read_text(encoding="utf-8")):
                target = target.strip("<>").split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                self.assertTrue((document.parent / target).resolve().exists(), f"{document}: {target}")

    def test_no_absolute_local_links_or_raw_html_archive(self):
        markdown = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.md"))
        self.assertIsNone(re.search(r"[A-Za-z]:[/\\]Users[/\\]", markdown))
        self.assertEqual(list(ROOT.rglob("*.html.gz")), [])

    def test_manifest_is_five_language_and_hashes_are_well_formed(self):
        rows = read_csv("audit/data/source-evidence-manifest.csv")
        self.assertTrue(rows)
        self.assertFalse(any("/th/" in f"/{row['relative_path']}" for row in rows))
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) for row in rows))
        self.assertTrue(all(row["stored_in_repository"] == "no" for row in rows))


if __name__ == "__main__":
    unittest.main(verbosity=2)
