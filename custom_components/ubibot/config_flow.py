"""Config flow for Ubibot integration."""
import logging
from typing import Any, Dict, Optional

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
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> Dict[str, Any]:
    """Validate the user input allows us to connect."""

    url = f"https://api.ubibot.io/channels/{data[CONF_CHANNEL]}?account_key={data[CONF_API_KEY]}"

    try:
        response = await hass.async_add_executor_job(
            requests.get, url
        )
        response.raise_for_status()

        if response.status_code == 200:
            return {"title": f"Ubibot Channel {data[CONF_CHANNEL]}"}

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            raise InvalidAuth from err
        raise CannotConnect from err
    except requests.exceptions.RequestException as err:
        raise CannotConnect from err


class UbibotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ubibot."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

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
