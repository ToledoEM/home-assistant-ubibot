# Ubibot integration for Home Assistant

## DEPRECATED not longer supported by Home Assistant 

This repo provides a plugin to work with Ubibot thermometers as sensors

## Installation

Install using HACS

## Configuration

Configure as a sensor in HA YAML configuration.yaml

```
sensor:
  platform: ubibot
  api_key: !secret ubibot_apikey
  channel: !secret ubibot_channel_number
  scan_interval: 900
```

Store secrets in secrets.yaml

```
ubibot_apikey: "YOUR_API_KEY" 
ubibot_channel_number: "YOUR_CHANNEL_NUMBER"
```

This version support external probe RS485 [link](https://store.ubibot.com/collections/external-sensors/products/temperature-and-humidity-probe)

To be Deprecated:

WARNING (ImportExecutor_0) [homeassistant.const] DEVICE_CLASS_HUMIDITY was used from ubibot, this is a deprecated constant which will be removed in HA Core 2025.1. Use SensorDeviceClass.HUMIDITY instead, please report it to the author of the 'ubibot' custom integration
WARNING (ImportExecutor_0) [homeassistant.const] DEVICE_CLASS_ILLUMINANCE was used from ubibot, this is a deprecated constant which will be removed in HA Core 2025.1. Use SensorDeviceClass.ILLUMINANCE instead, please report it to the author of the 'ubibot' custom integration
WARNING (ImportExecutor_0) [homeassistant.const] DEVICE_CLASS_TEMPERATURE was used from ubibot, this is a deprecated constant which will be removed in HA Core 2025.1. Use SensorDeviceClass.TEMPERATURE instead, please report it to the author of the 'ubibot' custom integration
WARNING (ImportExecutor_0) [homeassistant.const] DEVICE_CLASS_SIGNAL_STRENGTH was used from ubibot, this is a deprecated constant which will be removed in HA Core 2025.1. Use SensorDeviceClass.SIGNAL_STRENGTH instead, please report it to the author of the 'ubibot' custom integration
WARNING (ImportExecutor_0) [homeassistant.const] TEMP_CELSIUS was used from ubibot, this is a deprecated constant which will be removed in HA Core 2025.1. Use UnitOfTemperature.CELSIUS instead, please report it to the author of the 'ubibot' custom integration
