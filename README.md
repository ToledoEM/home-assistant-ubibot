# Ubibot Integration for Home Assistant

![ubibot](https://toledoem.github.io/img/logo.png "Ubibot")

A Home Assistant integration for Ubibot IoT environmental sensors, providing real-time monitoring of temperature, humidity, light levels, and more.

## Supported Devices

- Ubibot WS1
- External RS485 probe ([Temperature & Humidity Probe](https://store.ubibot.com/collections/external-sensors/products/temperature-and-humidity-probe))

## Available Sensors

Each Ubibot device will create the following sensors in Home Assistant:

| Sensor                 | Description                               | Unit |
| ---------------------- | ----------------------------------------- | ---- |
| Temperature (Internal) | Internal temperature sensor               | °C   |
| Temperature (External) | External probe temperature (if connected) | °C   |
| Humidity (Internal)    | Internal humidity sensor                  | %    |
| Humidity (External)    | External probe humidity (if connected)    | %    |
| Light Level            | Ambient light sensor                      | lux  |
| WiFi Signal            | WiFi signal strength                      | dBm  |

External probe sensors are created by the integration, but they may stay unavailable until a compatible probe is connected and the device reports those values.

## Requirements

Before installing, you'll need:

- A Ubibot account
- Your Ubibot Account Key
- Your device's Channel ID

## Installation

### HACS Installation (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed
2. Open HACS and go to "Integrations"
3. Open the top-right menu and choose "Custom repositories"
4. Add `https://github.com/ToledoEM/home-assistant-ubibot`
5. Select "Integration" as the category
6. Search for "Ubibot" in HACS and click "Download"
7. Restart Home Assistant

This repository is intended for HACS custom repository installation. Inclusion in the default HACS store requires additional review and branding requirements.

### Manual Installation

1. Download this repository
2. Copy the `custom_components/ubibot` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

The Ubibot integration is configured through the Home Assistant UI:

1. Go to Settings > Devices & Services
2. Click "+ ADD INTEGRATION"
3. Search for "Ubibot"
4. Enter:
   - Account Key (from your Ubibot account)
   - Channel ID (from your device settings)
   - Update Interval (optional, defaults to 300 seconds)

To find your Account Key and Channel ID:

1. Log in to [Ubibot Cloud](https://console.ubibot.com)
2. Go to "Account Settings" -> "Security Settings" for your Account Key
3. Go to "Console Dashboard" and select your device for the Channel ID

## Troubleshooting

Common issues and solutions:

### No Sensors Appear

- Verify your Account Key and Channel ID
- Check if your Ubibot device is online
- Look for errors in Home Assistant logs
- Ensure your device is reporting data to Ubibot Cloud

### Sensor Updates Are Delayed

- Check your network connection
- Verify the Update Interval setting
- Ensure your Ubibot device is actively reporting

### Error Messages

- "Invalid auth": Check your Account Key
- "Cannot connect": Verify your internet connection and Channel ID
- "Unknown": Check Home Assistant logs for detailed error messages

## Contributing

This integration is based on the work of [@ms32035](https://github.com/ms32035/home-assistant-ubibot) and welcomes community contributions.

To contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

### HACS Publication

This integration is ready for HACS (Home Assistant Community Store). Submission notes are summarized below.

**Quick steps:**
- Repository meets HACS requirements (hacs.json, manifest.json, workflows)
- Users can add it as a custom repository immediately
- To add to HACS defaults, submit a PR to [hacs/default](https://github.com/hacs/default)

## Support

- Report issues on [GitHub](https://github.com/ToledoEM/home-assistant-ubibot/issues)
- Read the [Ubibot API Documentation](https://www.ubibot.io/platform-api/)

## Releases & Versioning

- Integration releases use semantic versioning (for example `0.5.1`)
- Git tags / GitHub releases should use the `vX.Y.Z` format (for example `v0.5.1`)
- The `manifest.json` version matches the integration release version (without the leading `v`)

## License

This project is licensed under the MIT License. See the LICENSE file for details.
