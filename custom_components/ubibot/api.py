"""Ubibot API client."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any
from urllib.parse import quote

import aiohttp

_LOGGER = logging.getLogger(__name__)

_API_BASE_URL = "https://api.ubibot.io"
_REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=10)


class UbibotApiError(Exception):
    """Base Ubibot API error."""


class UbibotAuthenticationError(UbibotApiError):
    """Authentication failed for the Ubibot API."""


class UbibotConnectionError(UbibotApiError):
    """Network or transport error while calling the Ubibot API."""


class UbibotResponseError(UbibotApiError):
    """Unexpected or invalid response from the Ubibot API."""


def _normalize_last_values(raw_last_values: Any) -> dict[str, Any]:
    """Normalize the Ubibot `last_values` field."""
    if raw_last_values is None:
        return {}

    if isinstance(raw_last_values, dict):
        return raw_last_values

    if isinstance(raw_last_values, str):
        if not raw_last_values.strip():
            return {}

        parsed = json.loads(raw_last_values)
        if isinstance(parsed, dict):
            return parsed

        raise UbibotResponseError("Ubibot last_values payload is not an object")

    raise UbibotResponseError("Ubibot last_values payload has unsupported type")


def normalize_channel_payload(payload: Any) -> dict[str, Any]:
    """Normalize a Ubibot channel payload for the integration."""
    if not isinstance(payload, dict):
        raise UbibotResponseError("Ubibot payload is not a JSON object")

    channel = payload.get("channel")
    if not isinstance(channel, dict):
        raise UbibotResponseError("Ubibot payload is missing channel data")

    normalized_payload = dict(payload)
    normalized_channel = dict(channel)
    normalized_channel["last_values"] = _normalize_last_values(
        channel.get("last_values")
    )
    normalized_payload["channel"] = normalized_channel
    return normalized_payload


class UbibotApiClient:
    """Async Ubibot API client."""

    def __init__(
        self, session: aiohttp.ClientSession, account_key: str, channel: str
    ) -> None:
        """Initialize the client."""
        self._session = session
        self._account_key = account_key
        self._channel = channel

    @property
    def channel(self) -> str:
        """Configured Ubibot channel id."""
        return self._channel

    async def async_get_channel_data(self) -> dict[str, Any]:
        """Fetch the latest channel payload."""
        url = f"{_API_BASE_URL}/channels/{quote(self._channel, safe='')}"

        try:
            async with self._session.get(
                url,
                params={"account_key": self._account_key},
                timeout=_REQUEST_TIMEOUT,
            ) as response:
                if response.status in (401, 403):
                    raise UbibotAuthenticationError(
                        f"Ubibot authentication failed for channel {self._channel}"
                    )

                response.raise_for_status()
                payload = await response.json(content_type=None)
                if isinstance(payload, dict) and payload.get("error"):
                    error_message = str(payload["error"])
                    if any(
                        token in error_message.lower()
                        for token in ("auth", "account", "key", "unauthorized")
                    ):
                        raise UbibotAuthenticationError(
                            f"Ubibot authentication failed for channel {self._channel}"
                        )
                    raise UbibotResponseError(
                        f"Ubibot API returned an error for channel {self._channel}: "
                        f"{error_message}"
                    )
                return normalize_channel_payload(payload)

        except UbibotAuthenticationError:
            raise
        except aiohttp.ClientResponseError as err:
            _LOGGER.debug(
                "Ubibot API HTTP error for channel %s: status=%s",
                self._channel,
                err.status,
            )
            raise UbibotConnectionError(
                f"Ubibot API HTTP error for channel {self._channel}: {err.status}"
            ) from err
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.debug(
                "Ubibot API connection error for channel %s: %s",
                self._channel,
                err,
            )
            raise UbibotConnectionError(
                f"Ubibot API connection error for channel {self._channel}"
            ) from err
        except (ValueError, TypeError, json.JSONDecodeError) as err:
            _LOGGER.debug(
                "Ubibot API invalid payload for channel %s: %s",
                self._channel,
                err,
            )
            raise UbibotResponseError(
                f"Ubibot API returned invalid payload for channel {self._channel}"
            ) from err
