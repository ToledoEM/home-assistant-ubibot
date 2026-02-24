"""Unit tests for Ubibot payload normalization helpers."""

from __future__ import annotations

import importlib.util
import pathlib
import unittest

MODULE_PATH = (
    pathlib.Path(__file__).resolve().parents[1] / "custom_components/ubibot/api.py"
)

_IMPORT_ERROR = None
_API_MODULE = None

try:
    spec = importlib.util.spec_from_file_location("ubibot_api", MODULE_PATH)
    assert spec and spec.loader
    _API_MODULE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_API_MODULE)
except Exception as err:  # pragma: no cover - environment dependent
    _IMPORT_ERROR = err


@unittest.skipIf(
    _IMPORT_ERROR is not None, f"api.py import unavailable: {_IMPORT_ERROR}"
)
class TestNormalizeChannelPayload(unittest.TestCase):
    """Test payload normalization for Ubibot responses."""

    def test_normalizes_last_values_json_string(self) -> None:
        payload = {
            "channel": {
                "full_serial": "ABC123",
                "last_values": '{"field1": {"value": "24.4"}}',
            }
        }

        normalized = _API_MODULE.normalize_channel_payload(payload)

        self.assertEqual(
            normalized["channel"]["last_values"]["field1"]["value"],
            "24.4",
        )

    def test_accepts_last_values_dict(self) -> None:
        payload = {
            "channel": {
                "full_serial": "ABC123",
                "last_values": {"field5": {"value": "-70"}},
            }
        }

        normalized = _API_MODULE.normalize_channel_payload(payload)

        self.assertEqual(
            normalized["channel"]["last_values"]["field5"]["value"],
            "-70",
        )

    def test_rejects_invalid_last_values_json(self) -> None:
        payload = {
            "channel": {
                "full_serial": "ABC123",
                "last_values": "{bad json",
            }
        }

        with self.assertRaises(_API_MODULE.UbibotResponseError):
            _API_MODULE.normalize_channel_payload(payload)
