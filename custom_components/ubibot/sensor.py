"""Ubibot sensor."""
from datetime import datetime, timedelta
import json
import logging
import threading

import aiohttp

from homeassistant.const import (
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import CONF_CHANNEL
from .const import SENSOR_TYPES, MODELS, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class UbibotData:
    """Ubibot data object."""

    URL = "https://api.ubibot.io/channels/{0}?account_key={1}"

    def __init__(
        self, hass: HomeAssistant, account_key: str, channel: str, scan_interval: int
    ):
        """Initialize the Ubibot data object."""
        self.hass = hass
        self.account_key = account_key
        self.channel = channel
        self.scan_interval = scan_interval
        self.data = None

    async def async_update(self) -> dict:
        """Update data via API."""
        try:
            url = self.URL.format(self.channel, self.account_key)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        data = json.loads(text)
                        if "channel" in data:
                            data["channel"]["last_values"] = json.loads(
                                data["channel"]["last_values"]
                            )
                            self.data = data
                            return data
                    _LOGGER.error("Ubibot API error: %s", resp.status)
        except Exception as err:
            _LOGGER.error("Error updating Ubibot data: %s", err)
        return None


class UbibotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Ubibot Sensor."""

    def __init__(self, coordinator, sensor_type, channel, ubibot_data):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._type = sensor_type
        self._channel = channel
        self._ubibot_data = ubibot_data
        self._attr_unique_id = f"{self._channel}_{self._type}"
        self._attr_name = f"Ubibot - {self._channel} - {self._type}"
        self._attr_device_class = SENSOR_TYPES[self._type]["class"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[self._type]["unit"]
        self._attr_icon = SENSOR_TYPES[self._type]["icon"]

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        try:
            return self._ubibot_data.data["channel"]["last_values"][
                SENSOR_TYPES[self._type]["field"]
            ]["value"]
        except (TypeError, KeyError) as err:
            _LOGGER.debug("Error getting state for %s: %s", self._type, err)
            return None

    @property
    def state_class(self):
        """Return sensor state class"""
        return SensorStateClass.MEASUREMENT

    @property
    def device_info(self):
        """Return device info."""
        try:
            return {
                "identifiers": {
                    ("ubibot", self._ubibot_data.data["channel"]["full_serial"])
                },
                "name": self._ubibot_data.data["channel"]["full_serial"],
                "manufacturer": "Ubibot",
                "model": MODELS.get(
                    self._ubibot_data.data["channel"].get("product_id"), "Unknown"
                ),
            }
        except (TypeError, KeyError) as err:
            _LOGGER.debug("Error getting device info: %s", err)
            return {}


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    api_key = config.get(CONF_API_KEY)
    channel = config.get(CONF_CHANNEL)
    scan_interval = config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    await async_setup_ubibot(hass, api_key, channel, scan_interval, async_add_entities)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ubibot sensors from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    channel = entry.data[CONF_CHANNEL]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    await async_setup_ubibot(hass, api_key, channel, scan_interval, async_add_entities)


async def async_setup_ubibot(
    hass: HomeAssistant,
    api_key: str,
    channel: str,
    scan_interval: int,
    async_add_entities,
) -> None:
    """Set up the Ubibot sensors."""
    ubibot_data = UbibotData(hass, api_key, channel, scan_interval)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ubibot",
        update_method=ubibot_data.async_update,
        update_interval=timedelta(seconds=scan_interval),
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(UbibotSensor(coordinator, sensor_type, channel, ubibot_data))

    async_add_entities(entities, False)
