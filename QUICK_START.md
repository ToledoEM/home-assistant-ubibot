# Quick Start Guide - Adding Ubibot to HACS

This is a quick reference for users who want to install the Ubibot integration using HACS.

## Installation (2 minutes)

### Step 1: Add Custom Repository

1. Open HACS in Home Assistant
2. Click the **3-dot menu (⋮)** in the top right corner
3. Select **"Custom repositories"**
4. In the dialog:
   - **Repository**: `https://github.com/ToledoEM/home-assistant-ubibot`
   - **Category**: Select **"Integration"**
5. Click **"Add"**

### Step 2: Install Integration

1. In HACS, click **"Explore & Download Repositories"**
2. Search for **"Ubibot"**
3. Click on **"Ubibot"**
4. Click **"Download"**
5. Restart Home Assistant

### Step 3: Configure Integration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ ADD INTEGRATION"**
3. Search for **"Ubibot"**
4. Enter your credentials:
   - **Account Key**: From Ubibot Cloud (Account Settings → Security Settings)
   - **Channel ID**: From Ubibot Console Dashboard (select your device)
   - **Update Interval**: (Optional) Default is 300 seconds (5 minutes)
5. Click **"Submit"**

## Finding Your Credentials

### Account Key
1. Log in to [Ubibot Cloud](https://console.ubibot.com)
2. Click on your username/avatar
3. Go to **"Account Settings"**
4. Go to **"Security Settings"**
5. Copy your **Account Key**

### Channel ID
1. In [Ubibot Console](https://console.ubibot.com)
2. Go to **"Console Dashboard"**
3. Click on your device
4. Look for **"Channel ID"** in the device details
5. Copy the Channel ID (it's usually a number)

## Available Sensors

After configuration, you'll see these sensors in Home Assistant:

| Sensor | Entity ID Example |
|--------|------------------|
| Temperature (Internal) | `sensor.ubibot_[channel]_temperature` |
| Temperature (External) | `sensor.ubibot_[channel]_temperature_external` |
| Humidity (Internal) | `sensor.ubibot_[channel]_humidity` |
| Humidity (External) | `sensor.ubibot_[channel]_humidity_external` |
| Light Level | `sensor.ubibot_[channel]_light` |
| WiFi Signal | `sensor.ubibot_[channel]_rssi` |

## Troubleshooting

### Integration Not Found
- Make sure you added the custom repository URL correctly
- Verify the category is set to "Integration"
- Try refreshing HACS or restarting Home Assistant

### Invalid Auth Error
- Double-check your Account Key (no spaces before/after)
- Verify your Account Key is active in Ubibot Cloud
- Try regenerating your Account Key in Ubibot Cloud

### Cannot Connect Error
- Verify your Channel ID is correct
- Check if your Ubibot device is online in Ubibot Cloud
- Ensure your Home Assistant has internet access
- Check Home Assistant logs for detailed error messages

### No Sensors Appear
- Wait a few minutes for the first update
- Check if your device is actively reporting data to Ubibot Cloud
- Restart Home Assistant
- Check Home Assistant logs for errors

## Support

- **Issues**: [GitHub Issues](https://github.com/ToledoEM/home-assistant-ubibot/issues)
- **Documentation**: [README](https://github.com/ToledoEM/home-assistant-ubibot#readme)
- **Ubibot Help**: [Ubibot API Documentation](https://www.ubibot.io/platform-api/)

## Version Information

- **Current Version**: 0.5.0
- **Minimum Home Assistant**: 2022.8.0
- **Supported Devices**: Ubibot WS1, External RS485 probes

---

**Note**: This integration is community-maintained and not officially supported by Ubibot.
