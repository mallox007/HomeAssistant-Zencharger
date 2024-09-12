from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity, EntityDescription

from .api import ZenchargerApi
from .api_update_coordinator import ZenchargerApiCoordinator
from ..const import DOMAIN
from .websocket import ZenchargerWebSocket


class ZenchargerApiEntity(Entity):
    """Base class for all Zencharger entities."""

    def __init__(
            self,
            zencharger: ZenchargerApiCoordinator,
            description: EntityDescription,
    ):
        """Initialize the entity"""
        self._zencharger = zencharger
        self.entity_description = description
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "Zencharger")},
            manufacturer="Zencharger",
            name="Zencharger".capitalize(),
        )
        self._attr_unique_id = f"{description.key}"

    @callback
    def update_from_latest_data(self) -> None:
        """Update the entity from the latest data."""
        raise NotImplementedError
