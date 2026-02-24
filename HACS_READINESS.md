# HACS Readiness Checklist

This document tracks the readiness of the Ubibot integration for HACS publication.

## ✅ Completed Requirements

### Repository Structure
- ✅ Public GitHub repository
- ✅ Single integration under `custom_components/ubibot/`
- ✅ All required Python files present (`__init__.py`, `sensor.py`, `config_flow.py`, `const.py`)

### Configuration Files
- ✅ **hacs.json** exists at repository root
  - ✅ Contains `name` field
  - ✅ Contains `render_readme` field
  - ✅ Contains `homeassistant` minimum version (2022.8.0)
- ✅ **manifest.json** contains all required fields:
  - ✅ domain: `ubibot`
  - ✅ name: `Ubibot`
  - ✅ documentation: Points to GitHub README
  - ✅ issue_tracker: GitHub issues URL
  - ✅ codeowners: `[@toledoem]`
  - ✅ version: `0.5.0`
  - ✅ config_flow: `true`
  - ✅ integration_type: `hub`
  - ✅ iot_class: `cloud_polling`

### Documentation
- ✅ **README.md** with comprehensive information:
  - ✅ Clear description
  - ✅ Supported devices
  - ✅ Installation instructions (HACS and manual)
  - ✅ Configuration guide
  - ✅ Troubleshooting section
  - ✅ HACS publication information
- ✅ HACS submission guidance documented (local/private notes optional)
- ✅ **LICENSE** file (MIT License)

### GitHub Actions
- ✅ HACS validation workflow (`.github/workflows/validate.yml`)
- ✅ Hassfest validation workflow (`.github/workflows/hassfest.yml`)

### Assets
- ✅ Logo file present (`custom_components/ubibot/logo.png`)
- ✅ Repository image (`newLogo_en.png`)

## 🔲 Remaining Tasks (User Action Required)

These tasks require actions that must be performed by the repository owner on GitHub:

### 1. Add GitHub Topics
- [ ] Go to repository settings
- [ ] Add topics: `home-assistant`, `hacs`, `home-assistant-integration`, `ubibot`, `iot`, `sensors`

### 2. Submit Logo to Home Assistant Brands
- [ ] Fork https://github.com/home-assistant/brands
- [ ] Create folder: `custom_integrations/ubibot/`
- [ ] Prepare and add logo files:
  - [ ] `icon.png` (256x256px minimum, square)
  - [ ] `logo.png` (wider format)
  - [ ] Optional: `icon@2x.png`, `logo@2x.png` (HD versions)
- [ ] Create Pull Request to brands repository
- [ ] Wait for PR approval and merge

### 3. Create GitHub Release
- [ ] Go to repository releases page
- [ ] Create new release with tag `v0.5.0`
- [ ] Add release notes describing features
- [ ] Publish release

### 4. Verify Workflows Pass
- [ ] Check GitHub Actions tab
- [ ] Ensure HACS validation passes ✅
- [ ] Ensure Hassfest validation passes ✅

### 5. Submit to HACS Default (Optional)
- [ ] Fork https://github.com/hacs/default
- [ ] Add `ToledoEM/home-assistant-ubibot` to `integration` file (alphabetically)
- [ ] Create Pull Request
- [ ] Fill out PR template completely
- [ ] Wait for review (can take weeks/months)

## 🎯 Immediate Next Steps

1. **Add GitHub Topics** (5 minutes)
   - Makes repository discoverable
   - Required for best practices

2. **Create GitHub Release** (10 minutes)
   - Allows version selection in HACS
   - Good practice for version management

3. **Test with HACS** (5 minutes)
   - Add as custom repository in HACS
   - Verify installation works correctly

## 📊 Current Status

**Repository is HACS-ready!** ✅

Users can install the integration immediately by adding it as a custom repository in HACS:
```
https://github.com/ToledoEM/home-assistant-ubibot
```

The integration meets all technical requirements for HACS. The remaining tasks are for:
- Enhanced discoverability (topics, brands logo)
- Version management (releases)
- HACS default repository inclusion (optional, for automatic discovery)

## 📚 References

- [HACS Publisher Documentation](https://hacs.xyz/docs/publish/)
- [Repository README](./README.md)

---

**Last Updated**: 2025-11-12
**Repository Status**: ✅ HACS-Ready (Custom Repository)
**Next Milestone**: Submit to HACS Default Repository
