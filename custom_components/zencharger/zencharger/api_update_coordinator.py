import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.zencharger.zencharger.api import ZenchargerApi

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)  # Adjust the interval as needed


class ZenchargerApiCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, zencharger_api: ZenchargerApi):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name="zencharger", update_interval=SCAN_INTERVAL,
                         update_method=self.async_poll_api)
        self._zencharger_api = zencharger_api

    def update_data(self):
        snapshot = self._zencharger_api.system_snapshot()

        # Process data and return what you need for sensors
        return {
            "currentPowerUsage1": float(snapshot['Signals'][0]['Value'][0]) * 230,
            "currentPowerUsage2": float(snapshot['Signals'][0]['Value'][1]) * 230,
            "currentPowerUsage3": float(snapshot['Signals'][0]['Value'][2]) * 230,
            # Extract more values as needed
        }

    async def async_poll_api(self):
        return await self.hass.async_add_executor_job(self.update_data)


