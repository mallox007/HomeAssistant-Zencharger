"""API client for Zencharger Dashboard."""

import logging

import httpx
from requests import get

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ..const import CONF_CREDENTIALS, CONF_DATA, CONF_HOST, CONF_PASSWORD
from .websocket import ZenchargerWebSocket
from .const import ATTR_DATA, ATTR_FAIL_CODE

_LOGGER = logging.getLogger(__name__)


class ZenchargerApi:
    """Api class."""

    @property
    def websocket(self):
        return self._websocket

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self._sessionId = None
        if isinstance(entry, dict):
            self._host = entry[CONF_DATA][CONF_CREDENTIALS][CONF_HOST]
            self._password = entry[CONF_DATA][CONF_CREDENTIALS][CONF_PASSWORD]
        else:            
            self._host = entry.data[CONF_CREDENTIALS][CONF_HOST]
            self._password = entry.data[CONF_CREDENTIALS][CONF_PASSWORD]

        self._websocket = ZenchargerWebSocket(hass, entry)

    async def ws_connect(self):
        if self._sessionId is None:
            self.login()
        await self._websocket.ws_connect(self._sessionId)

    def login(self) -> str:
        """Login to api to get Session id."""

        url = self._host + "/api/v1/auth/login"
        headers = {
            "accept": "application/json",
        }
        body = {
            "Password": self._password,
            "PersistentSession": True,
        }
        try:
            response = httpx.post(url, headers=headers, json=body, timeout=1.5)
            response.raise_for_status()

            if "Set-Cookie" in response.headers:
                self._sessionId = response.headers["Set-Cookie"]
                return response.headers.get("Set-Cookie")

            raise ZenchargerApiError("Could not login with given credentials")
        except Exception as error:
            raise ZenchargerApiError("Could not login with given credentials")

    def status(self) -> str:
        """Get status from API."""

        url = self._host + "/api/v1/auth/status"
        headers = {
            "accept": "application/json",
        }

        try:
            response = get(url, headers=headers, timeout=1.5)
            response.raise_for_status()

            if "Set-Cookie" in response.headers:
                self._sessionId = response.headers["Set-Cookie"]
                return response.headers.get("Set-Cookie")

            raise ZenchargerApiError("Could not get status")
        except Exception as error:
            raise ZenchargerApiError("Could not get status")

    def system_snapshot(self) -> dict:
        """Get system snapshot from API."""

        return self._do_call(self._host + '/api/v1/system/diagnostics/snapshot')

    def _do_call(self, url: str):
        if self._sessionId is None:
            self.login()

        headers = {
            "accept": "application/json",
            "cookie": self._sessionId,
        }

        try:
            response = httpx.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            json_data = response.json()

            return json_data

        except KeyError as error:
            _LOGGER.error(error)
            _LOGGER.error(response.text)


class ZenchargerApiError(Exception):
    """Generic Zencharger Api error."""


class ZenchargerApiAccessFrequencyTooHighError(ZenchargerApiError):
    pass


class ZenchargerApiErrorInvalidAccessToCurrentInterfaceError(ZenchargerApiError):
    pass
