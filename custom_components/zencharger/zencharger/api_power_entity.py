from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfPower
from homeassistant.helpers.entity import EntityDescription

from .api import ZenchargerApi
from .api_entity import ZenchargerApiEntity
from .api_update_coordinator import ZenchargerApiCoordinator
from .entity import ZenchargerEntity
from .websocket import ZenchargerWebSocket


class ZenchargerApiPowerEntity(ZenchargerApiEntity):
    """Base class for all ZenchargerApiPowerEntity entities."""

    def __init__(
            self,
            zencharger: ZenchargerApiCoordinator,
            description: EntityDescription,
    ):
        """Initialize the entity"""
        super().__init__(zencharger, description)

    @property
    def device_class(self):
        return SensorDeviceClass.POWER

    @property
    def unit_of_measurement(self):
        return UnitOfPower.WATT


class ZenchargerPowerEntityRealtime(ZenchargerApiPowerEntity):
    pass


class ZenchargerPowerEntityRealtimeInWatt(ZenchargerApiPowerEntity):
    @property
    def unit_of_measurement(self):
        return UnitOfPower.WATT
