"""Constants for Ubibot module."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    UnitOfIlluminance,
    UnitOfSignalStrength,
    UnitOfTemperature,
)

DOMAIN = "ubibot"
CONF_CHANNEL = "channel"
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

SENSOR_TYPES = {
    "temperature": {
        "class": SensorDeviceClass.TEMPERATURE,
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "field": "field1",
    },
    "temperature_ext": {
        "class": SensorDeviceClass.TEMPERATURE,
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "field": "field9",
    },
     "humidity_ext": {
        "class": SensorDeviceClass.HUMIDITY,
        "unit": "%",
        "icon": "mdi:water-percent",
        "field": "field10",
    },
    "humidity": {
        "class": SensorDeviceClass.HUMIDITY,
        "unit": "%",
        "icon": "mdi:water-percent",
        "field": "field2",
    },
    "lux": {
        "class": SensorDeviceClass.ILLUMINANCE,
        "unit": UnitOfIlluminance.LUX,
        "icon": "mdi:lightbulb-on-outline",
        "field": "field3",
    },
    "wifi_rssi": {
        "class": SensorDeviceClass.SIGNAL_STRENGTH,
        "unit": UnitOfSignalStrength.DECIBEL_MILLIWATT,
        "icon": "mdi:wifi",
        "field": "field5",
    },
}

MODELS = {"ubibot-ws1": "WS1"}
