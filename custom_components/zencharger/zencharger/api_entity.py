from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api_update_coordinator import ZenchargerApiCoordinator
from ..const import DOMAIN


class ZenchargerApiEntity(CoordinatorEntity):
    """Base class for all Zencharger entities."""

    def __init__(
            self,
            coordinator: ZenchargerApiCoordinator,
            description: EntityDescription,
    ):
        super().__init__(coordinator, description)
        """Initialize the entity"""
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
