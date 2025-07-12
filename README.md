# Ubibot Integration for Home Assistant

![ubibot](newLogo_en.png "Ubibot")

This integration allows you to integrate your Ubibot sensors with Home Assistant, providing real-time monitoring of temperature, humidity, light levels, and WiFi signal strength.

## Features

- Support for Ubibot WS1 devices
- Temperature and humidity monitoring (internal and external probe)
- Light level monitoring
- WiFi signal strength monitoring
- Configurable update intervals
- UI-based configuration
- Support for external RS485 probe ([link](https://store.ubibot.com/collections/external-sensors/products/temperature-and-humidity-probe))

## Installation

### Using HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the "+" button
4. Search for "Ubibot"
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/ubibot` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### Using the UI (Recommended)

1. Go to Configuration > Integrations
2. Click the "+ ADD INTEGRATION" button
3. Search for "Ubibot"
4. Enter your:
   - Account Key (from your Ubibot account)
   - Channel ID (from your device)
   - Update Interval (optional, defaults to 300 seconds)

### Using configuration.yaml (Legacy Method)

While UI configuration is recommended, YAML configuration is still supported:

```yaml
sensor:
  platform: ubibot
  api_key: !secret ubibot_apikey
  channel: !secret ubibot_channel_number
  scan_interval: 900  # optional, defaults to 300 seconds
```

And in your `secrets.yaml`:
```yaml
ubibot_apikey: "YOUR_API_KEY" 
ubibot_channel_number: "YOUR_CHANNEL_NUMBER"
```

## Available Sensors

The integration will automatically create sensors for:
- Temperature (internal and external probe if connected)
- Humidity (internal and external probe if connected)
- Light level (lux)
- WiFi signal strength (RSSI)

## Troubleshooting

If you encounter any issues:
1. Check your Account Key and Channel ID
2. Verify your Ubibot device is online and reporting data
3. Check the Home Assistant logs for any error messages

## Contributing

Feel free to contribute to this integration by:
1. Reporting issues
2. Suggesting new features
3. Creating pull requests

## License

This integration is licensed under MIT License.
