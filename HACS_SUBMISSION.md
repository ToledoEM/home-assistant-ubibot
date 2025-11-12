# HACS Submission Guide

This document provides step-by-step instructions for submitting the Ubibot integration to HACS (Home Assistant Community Store).

## Prerequisites Checklist

Before submitting to HACS, ensure the following requirements are met:

- [x] Repository is public on GitHub
- [x] Repository has a clear description
- [x] `hacs.json` file exists at repository root
- [x] `manifest.json` exists in `custom_components/ubibot/`
- [x] `README.md` with clear installation and configuration instructions
- [x] GitHub Actions workflows for validation (HACS and hassfest)
- [ ] Logo submitted to home-assistant/brands repository
- [ ] GitHub repository topics are set
- [ ] Create a GitHub release
- [ ] Submit to HACS default repository

## Step 1: Add GitHub Topics

Add relevant topics to make your repository discoverable:

1. Go to https://github.com/ToledoEM/home-assistant-ubibot
2. Click "⚙️ Settings" (or edit repository details)
3. Add the following topics:
   - `home-assistant`
   - `hacs`
   - `home-assistant-integration`
   - `ubibot`
   - `iot`
   - `sensors`

## Step 2: Submit Logo to Home Assistant Brands Repository

The logo must be added to the official brands repository for it to appear in the Home Assistant UI.

### 2.1 Prepare Logo Files

Your integration already has `logo.png` in `custom_components/ubibot/`. You'll need to prepare:

- `icon.png` - Square icon (minimum 256x256px, transparent background)
- `logo.png` - Wider logo format (transparent background)

Optional (for better appearance):
- `icon@2x.png` - High DPI version (512x512px)
- `logo@2x.png` - High DPI logo

### 2.2 Submit to Brands Repository

1. Fork the repository: https://github.com/home-assistant/brands
2. Create a new folder: `custom_integrations/ubibot/`
3. Add your logo files to this folder
4. Create a Pull Request with the title: "Add Ubibot custom integration"
5. Wait for the PR to be reviewed and merged

**Important**: The logo will only appear in Home Assistant after the PR is merged and the brands repository is updated.

## Step 3: Create a GitHub Release

Releases allow users to install specific versions of your integration.

1. Go to https://github.com/ToledoEM/home-assistant-ubibot/releases
2. Click "Draft a new release"
3. Create a new tag (e.g., `v0.5.0` matching the version in manifest.json)
4. Release title: `Release 0.5.0` or `Ubibot v0.5.0`
5. Add release notes describing features and changes:

```markdown
## Features
- Temperature monitoring (internal and external probe)
- Humidity monitoring (internal and external probe)
- Light level monitoring
- WiFi signal strength monitoring
- Full Home Assistant UI configuration
- Automatic device discovery

## Supported Devices
- Ubibot WS1
- External RS485 Temperature & Humidity Probe

## Requirements
- Home Assistant 2022.8.0 or newer
- Ubibot account with Account Key
- Device Channel ID
```

6. Click "Publish release"

## Step 4: Test HACS Validation

Before submitting, ensure all validations pass:

```bash
# The repository already has GitHub Actions configured
# Check the Actions tab: https://github.com/ToledoEM/home-assistant-ubibot/actions

# You should see:
# ✅ HACS validation passing
# ✅ Hassfest validation passing
```

## Step 5: Submit to HACS Default Repository

To make your integration discoverable in HACS without users needing to add a custom repository:

### 5.1 Fork HACS Default Repository

1. Go to https://github.com/hacs/default
2. Click "Fork" to create your own copy

### 5.2 Add Your Integration

1. In your fork, edit the file `integration` (no extension)
2. Add your repository URL alphabetically to the list:

```
ToledoEM/home-assistant-ubibot
```

The file is a simple list of GitHub repository paths (one per line), sorted alphabetically.

### 5.3 Create Pull Request

1. Commit your changes with message: "Add ToledoEM/home-assistant-ubibot"
2. Create a Pull Request from your fork to `hacs/default`
3. Fill out the PR template completely:
   - Repository URL: https://github.com/ToledoEM/home-assistant-ubibot
   - Category: Integration
   - Description: Brief description of the integration
   - Confirm all checkboxes in the PR template

### 5.4 PR Requirements

**Important**: Only repository owners or major contributors can submit PRs. PRs from organization accounts are not accepted.

The PR will be reviewed by HACS maintainers. This process can take weeks or months due to review backlogs.

## Alternative: Manual Installation (Available Immediately)

Users can install your integration immediately without waiting for HACS approval:

### For Users:

1. In HACS, click the 3-dot menu (⋮) in the top right
2. Select "Custom repositories"
3. Add repository URL: `https://github.com/ToledoEM/home-assistant-ubibot`
4. Category: Integration
5. Click "Add"
6. The integration will now appear in HACS for download

This method works immediately and doesn't require approval, but users must manually add the repository.

## Verification Checklist

Before submitting, verify:

- [ ] All GitHub Actions pass (green checkmarks)
- [ ] README is comprehensive and up-to-date
- [ ] `hacs.json` contains required fields
- [ ] `manifest.json` contains all required fields
- [ ] At least one GitHub release is published
- [ ] Repository has appropriate topics
- [ ] Logo submitted to brands repository (or in progress)

## Resources

- [HACS Publisher Documentation](https://hacs.xyz/docs/publish/)
- [HACS Integration Requirements](https://hacs.xyz/docs/publish/integration/)
- [Home Assistant Brands Repository](https://github.com/home-assistant/brands)
- [HACS Default Repository](https://github.com/hacs/default)

## Support

If you encounter issues during submission:
- Check HACS documentation: https://hacs.xyz/docs/
- Ask in HACS Discord: https://discord.gg/apgchf8
- Open an issue in HACS: https://github.com/hacs/integration/issues

## Timeline

- **Immediate**: Users can add as custom repository
- **Brands PR**: Usually reviewed within days to weeks
- **HACS Default PR**: Can take weeks to months for approval

Once approved and added to HACS defaults, your integration will be discoverable by all HACS users without any manual repository addition.
