"""Ubibot sensor."""
from datetime import datetime, timedelta
import json
import logging
import threading

import requests

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

from . import CONF_CHANNEL
from .const import SENSOR_TYPES, MODELS

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Ubibot sensor setup."""

    api_key = config.get(CONF_API_KEY)
    channel = config.get(CONF_CHANNEL)
    scan_interval = config.get(CONF_SCAN_INTERVAL)

    ubibot_data = UbibotData(api_key, channel, scan_interval)

    entities = []
    for t in SENSOR_TYPES:
        entities.append(UbibotSensor(t, channel, ubibot_data))
    
    async_add_entities(entities, True)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Ubibot sensors from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    channel = entry.data[CONF_CHANNEL]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL)

    ubibot_data = UbibotData(api_key, channel, scan_interval)

    entities = []
    for t in SENSOR_TYPES:
        entities.append(UbibotSensor(t, channel, ubibot_data))
    
    async_add_entities(entities, True)


class UbibotSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, sensor_type, channel, ubibot_data):
        """Initialize the sensor."""
        self._type = sensor_type
        self._channel = channel
        self._ubibot_data = ubibot_data
        self._state = None
        try:
            self._state = self._ubibot_data.data["channel"]["last_values"][SENSOR_TYPES[self._type]["field"]]["value"]
        except (TypeError, KeyError, ValueError) as err:
            _LOGGER.error(f"UbibotSensor init error for {self._type}: {err}")
            self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Ubibot - {self._channel} - {self._type}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self._state

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._type]["class"]

    @property
    def native_unit_of_measurement(self):
        """Return the native unit of measurement."""
        return SENSOR_TYPES[self._type]["unit"]

    @property
    def icon(self):
        """Return the icon."""
        return SENSOR_TYPES[self._type]["icon"]

    @property
    def unique_id(self) -> str:
        """Return the unique id."""
        return f"{self._channel}_{self._type}"

    def update(self):
        """Fetch new state data for the sensor."""
        self._ubibot_data.update()
        try:
            self._state = self._ubibot_data.data["channel"]["last_values"][SENSOR_TYPES[self._type]["field"]]["value"]
        except (TypeError, KeyError, ValueError) as err:
            _LOGGER.error(f"UbibotSensor update error for {self._type}: {err}")
            self._state = None

    @property
    def state_class(self):
        """Return sensor state class"""
        return SensorStateClass.MEASUREMENT

    @property
    def device_info(self):
        """Return device"""
        try:
            return {
                "identifiers": {
                    ("ubibot", self._ubibot_data.data["channel"]["full_serial"])
                },
                "name": self._ubibot_data.data["channel"]["full_serial"],
                "firmware": self._ubibot_data.data["channel"]["firmware"],
                "manufacturer": "Ubibot",
                "model": MODELS.get(self._ubibot_data.data["channel"].get("product_id"), "Unknown"),
            }
        except (TypeError, KeyError) as err:
            _LOGGER.error(f"UbibotSensor device_info error: {err}")
            return {}


class UbibotData:
    """Ubibot data object."""

    URL = "https://api.ubibot.io/channels/{0}?account_key={1}"

    def __init__(self, account_key, channel, scan_interval):
        """
        Initialize the UniFi Ubibot data object.

        :param account_key: Ubibot Account Key
        :param channel: Channel ID
        :param scan_interval: refresh interval in seconds
        """
        self.account_key = account_key
        self.channel = channel
        self.scan_interval = scan_interval
        self.last_refresh = datetime(2000, 1, 1)
        self.data = None
        self._update_in_progress = threading.Lock()
        self.update()

    def update(self):
        """Get data from Ubibot API."""
        if (
            datetime.now() < self.last_refresh + timedelta(seconds=self.scan_interval)
            or not self._update_in_progress.acquire(False)
        ):
            return
        try:
            url = UbibotData.URL.format(self.channel, self.account_key)
            r = requests.get(url)
            if r.status_code == 200:
                try:
                    self.data = json.loads(r.text)
                    self.data["channel"]["last_values"] = json.loads(
                        self.data["channel"]["last_values"]
                    )
                except (KeyError, ValueError, TypeError) as err:
                    _LOGGER.error(f"UbibotData API response error: {err}")
                    self.data = None
            else:
                _LOGGER.error(f"Ubibot API error: {r.status_code}")
            self.last_refresh = datetime.now()
        except Exception as err:
            _LOGGER.error(f"UbibotData update exception: {err}")
        finally:
            self._update_in_progress.release()
