"""Ubibot sensor."""

import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_CHANNEL, DOMAIN, MODELS, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


class UbibotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Ubibot Sensor."""

    def __init__(self, coordinator, sensor_type: str, channel: str):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._type = sensor_type
        self._channel = channel
        self._attr_unique_id = f"{self._channel}_{self._type}"
        self._attr_name = f"Ubibot - {self._channel} - {self._type}"
        self._attr_device_class = SENSOR_TYPES[self._type]["class"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[self._type]["unit"]
        self._attr_icon = SENSOR_TYPES[self._type]["icon"]
        self._attr_state_class = SensorStateClass.MEASUREMENT

        if self._type == "wifi_rssi":
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        try:
            field_name = SENSOR_TYPES[self._type]["field"]
            field_data = self.coordinator.data["channel"]["last_values"][field_name]
            if not isinstance(field_data, dict):
                return None
            return self._coerce_numeric_value(field_data.get("value"))
        except (TypeError, KeyError) as err:
            _LOGGER.debug("Error getting state for %s: %s", self._type, err)
            return None

    def _coerce_numeric_value(self, value):
        """Coerce Ubibot string values into numeric Home Assistant sensor values."""
        if value is None or isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            numeric = float(value)
        elif isinstance(value, str):
            if not value.strip():
                return None
            try:
                numeric = float(value)
            except ValueError:
                _LOGGER.debug("Invalid numeric value for %s: %s", self._type, value)
                return None
        else:
            _LOGGER.debug(
                "Unsupported value type for %s: %s",
                self._type,
                type(value),
            )
            return None

        if self._type == "wifi_rssi":
            return int(numeric)

        return numeric

    @property
    def device_info(self):
        """Return device info."""
        try:
            channel_data = self.coordinator.data["channel"]
            serial = channel_data["full_serial"]
            return {
                "identifiers": {(DOMAIN, serial)},
                "name": serial,
                "manufacturer": "Ubibot",
                "model": MODELS.get(
                    channel_data.get("product_id"), "Unknown"
                ),
            }
        except (TypeError, KeyError) as err:
            _LOGGER.debug("Error getting device info: %s", err)
            return {}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ubibot sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    channel = entry.data[CONF_CHANNEL]

    async_add_entities(
        [
            UbibotSensor(coordinator, sensor_type, channel)
            for sensor_type in SENSOR_TYPES
        ]
    )
