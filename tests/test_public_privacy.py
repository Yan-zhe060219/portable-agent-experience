from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).parents[1] / "skills" / "experience-distiller" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_library import validate_file


class PublicPrivacyTests(unittest.TestCase):
    def test_flags_possible_public_absolute_path(self):
        fixture = Path(__file__).parent / "fixtures" / "valid" / "candidate-script.md"
        text = fixture.read_text(encoding="utf-8").replace("Fixture only.", "C:\\Users\\example", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "card.md"
            path.write_text(text, encoding="utf-8")
            self.assertIn("possible public privacy issue: absolute path", validate_file(path))
