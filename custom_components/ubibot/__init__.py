"""Ubibot component."""
from __future__ import annotations

import logging
from datetime import timedelta

import requests

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, CONF_CHANNEL, DEFAULT_SCAN_INTERVAL

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Ubibot from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Test the connection
    try:
        url = f"https://api.ubibot.io/channels/{entry.data[CONF_CHANNEL]}?account_key={entry.data[CONF_API_KEY]}"
        response = await hass.async_add_executor_job(requests.get, url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise ConfigEntryNotReady from err

    hass.data[DOMAIN][entry.entry_id] = {
        CONF_API_KEY: entry.data[CONF_API_KEY],
        CONF_CHANNEL: entry.data[CONF_CHANNEL],
        CONF_SCAN_INTERVAL: entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
