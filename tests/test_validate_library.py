from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).parents[1] / "skills" / "experience-distiller" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_library import validate_file


FIXTURES = Path(__file__).parent / "fixtures"


class ValidateLibraryTests(unittest.TestCase):
    def test_accepts_valid_candidate(self):
        self.assertEqual([], validate_file(FIXTURES / "valid" / "candidate-script.md"))

    def test_rejects_missing_proposed_kind(self):
        errors = validate_file(FIXTURES / "invalid" / "missing-proposed-kind.md")
        self.assertIn("missing required key: proposed_kind", errors)

    def test_rejects_invalid_id(self):
        errors = validate_file(FIXTURES / "invalid" / "invalid-id.md")
        self.assertIn("invalid id", errors)

    def test_rejects_missing_required_section(self):
        errors = validate_file(FIXTURES / "invalid" / "missing-section.md")
        self.assertIn("missing section: ## Risks and rollback", errors)

    def test_rejects_non_utf8_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "non-utf8.md"
            path.write_bytes(b"\xff")

            self.assertEqual(["file is not valid UTF-8"], validate_file(path))
