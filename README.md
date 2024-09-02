# Ubibot integration for Home Assistant

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
