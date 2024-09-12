"""Zencharger sensor."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ZenchargerConfigEntry
from .const import (
    ID_INSTANTANEOUS_POWER,
    ID_INSTANTANEOUS_POWER_PHASE_1,
    ID_INSTANTANEOUS_POWER_PHASE_2,
    ID_INSTANTANEOUS_POWER_PHASE_3,
    ID_SESSION_ENERGY,
    ID_STATE,
    ID_TOTAL_ENERGY, ID_CURRENT_POWER_USAGE_PHASE_1, ID_CURRENT_POWER_USAGE_PHASE_2, ID_CURRENT_POWER_USAGE_PHASE_3,
)
from .zencharger.api_power_sensor import ZenchargerApiPowerSensor
from .zencharger.api_update_coordinator import ZenchargerApiCoordinator
from .zencharger.energy_sensor import ZenchargerEnergySensor
from .zencharger.power_sensor import ZenchargerPowerSensor
from .zencharger.sensor import ZenchargerSensor

_LOGGER = logging.getLogger(__name__)

SENSOR_DESCRIPTIONS = SensorEntityDescription(
    key=ID_STATE,
    translation_key="state",
    name="State",
)
ENERGY_SENSOR_DESCRIPTIONS = (
    SensorEntityDescription(
        key=ID_TOTAL_ENERGY,
        translation_key="total",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        name="Total energy",
    ),
    SensorEntityDescription(
        key=ID_SESSION_ENERGY,
        translation_key="session",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        name="Session energy",
    ),
)
POWER_SENSOR_DESCRIPTIONS = (
    SensorEntityDescription(
        key=ID_INSTANTANEOUS_POWER,
        translation_key="instant",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        name="Instantaneous power",
    ),
    SensorEntityDescription(
        key=ID_INSTANTANEOUS_POWER_PHASE_1,
        translation_key="instantPhase1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        name="Instantaneous power, phase 1",
    ),
    SensorEntityDescription(
        key=ID_INSTANTANEOUS_POWER_PHASE_2,
        translation_key="instantPhase2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        name="Instantaneous power, phase 2",
    ),
    SensorEntityDescription(
        key=ID_INSTANTANEOUS_POWER_PHASE_3,
        translation_key="instantPhase3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        name="Instantaneous power, phase 3",
    )
)

API_POWER_SENSORY_DESCRIPTORS = (
    SensorEntityDescription(
        key=ID_CURRENT_POWER_USAGE_PHASE_1,
        translation_key="currentPhase1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        name="current power, phase 1",
    ),
    SensorEntityDescription(
        key=ID_CURRENT_POWER_USAGE_PHASE_2,
        translation_key="currentPhase2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        name="current power, phase 2",
    ),
    SensorEntityDescription(
        key=ID_CURRENT_POWER_USAGE_PHASE_3,
        translation_key="currentPhase3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        name="current power, phase 3",
    )
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ZenchargerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up zencharger sensors based on a config entry."""
    zencharger = entry.runtime_data.websocket
    zenchargerApi = entry.runtime_data

    async_add_entities(
        ZenchargerEnergySensor(zencharger, description)
        for description in ENERGY_SENSOR_DESCRIPTIONS
    )
    async_add_entities(
        ZenchargerPowerSensor(zencharger, description)
        for description in POWER_SENSOR_DESCRIPTIONS
    )

    coordinator = ZenchargerApiCoordinator(hass,zenchargerApi)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities(
        ZenchargerApiPowerSensor(coordinator, description)
        for description in API_POWER_SENSORY_DESCRIPTORS
    )
    async_add_entities([ZenchargerSensor(zencharger, SENSOR_DESCRIPTIONS)])
