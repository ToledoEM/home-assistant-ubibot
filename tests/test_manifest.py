"""Repository metadata tests."""

from __future__ import annotations

import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class TestManifest(unittest.TestCase):
    """Validate integration manifest metadata."""

    def test_manifest_has_required_publish_metadata(self) -> None:
        manifest = json.loads(
            (ROOT / "custom_components/ubibot/manifest.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(manifest["domain"], "ubibot")
        self.assertEqual(manifest["integration_type"], "hub")
        self.assertNotIn("requirements", manifest)
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(
            manifest["documentation"],
            "https://github.com/ToledoEM/home-assistant-ubibot",
        )

    def test_license_file_exists(self) -> None:
        self.assertTrue((ROOT / "LICENSE").is_file())


class TestHacsMetadata(unittest.TestCase):
    """Validate minimal HACS metadata file."""

    def test_hacs_json_parses(self) -> None:
        data = json.loads((ROOT / "hacs.json").read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "Ubibot")
        self.assertTrue(data["render_readme"])
