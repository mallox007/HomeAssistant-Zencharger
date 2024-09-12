import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityDescription

from .api import ZenchargerApi
from .api_power_entity import ZenchargerApiPowerEntity
from .api_update_coordinator import ZenchargerApiCoordinator
from .power_entity import ZenchargerPowerEntity
from .websocket import ZenchargerWebSocket

_LOGGER = logging.getLogger(__name__)


class ZenchargerApiPowerSensor(ZenchargerApiPowerEntity, SensorEntity):
    """Base class for all ZenchargerPowerSensor sensors."""

    def __init__(
            self,
            coordinator: ZenchargerApiCoordinator,
            description: EntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, description)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor."""
        raw = self.coordinator.data.get(self.entity_description.key)
        self._attr_native_value = raw
        self.async_write_ha_state()
