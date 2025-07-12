"""Config flow for Ubibot integration."""
from __future__ import annotations

import logging
from typing import Any

import requests
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_CHANNEL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_CHANNEL): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=60)
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    url = f"https://api.ubibot.io/channels/{data[CONF_CHANNEL]}?account_key={data[CONF_API_KEY]}"

    try:
        response = await hass.async_add_executor_job(requests.get, url)
        response.raise_for_status()
        json_response = response.json()

        if "error" in json_response:
            raise InvalidAuth

        return {"title": f"Ubibot Channel {data[CONF_CHANNEL]}"}

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            raise InvalidAuth from err
        raise CannotConnect from err
    except (requests.exceptions.RequestException, ValueError) as err:
        raise CannotConnect from err


@config_entries.HANDLERS.register(DOMAIN)
class UbibotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ubibot."""

    VERSION = 1

    async def async_step_import(self, import_data: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_data)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                await self.async_set_unique_id(user_input[CONF_CHANNEL])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)

            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
