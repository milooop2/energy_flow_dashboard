"""Automatic Lovelace resource registration for EnergyFlowDashboard."""

import logging

from homeassistant.components.lovelace import DOMAIN as LOVELACE_DOMAIN
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant, callback

_LOGGER = logging.getLogger(__name__)

RESOURCE_URL = "/energy_flow_dashboard/frontend/energy-flow-dashboard.js"
RESOURCE_TYPE = "module"


async def async_register_lovelace_resource(hass: HomeAssistant) -> None:
    """Register the JS module as a Lovelace resource."""
    if not hass.is_running:
        @callback
        def _started(_event):
            hass.async_create_task(_do_register(hass))

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _started)
    else:
        await _do_register(hass)


async def _do_register(hass: HomeAssistant) -> None:
    """Actually register the resource."""
    lovelace_data = hass.data.get(LOVELACE_DOMAIN)
    if lovelace_data is None:
        _LOGGER.warning(
            "EnergyFlowDashboard: Lovelace data not available; "
            "add the resource manually in Settings -> Dashboards -> Resources."
        )
        return

    # In HA 2026.x lovelace_data.resources is the global resource collection
    resources = getattr(lovelace_data, "resources", None)
    if resources is None:
        _LOGGER.warning(
            "EnergyFlowDashboard: lovelace_data.resources not available; "
            "add the resource manually."
        )
        return

    # Check if the collection supports creating items (storage mode only)
    if not hasattr(resources, "async_create_item"):
        _LOGGER.info(
            "EnergyFlowDashboard: Lovelace is in YAML mode; add the "
            "resource manually to configuration.yaml: url: %s type: %s",
            RESOURCE_URL,
            RESOURCE_TYPE,
        )
        return

    # Check if already registered
    try:
        existing = resources.async_items()
    except Exception as err:  # noqa: BLE001
        _LOGGER.error(
            "EnergyFlowDashboard: could not list Lovelace resources: %s", err
        )
        return

    for item in existing:
        if item.get("url") == RESOURCE_URL:
            _LOGGER.info(
                "EnergyFlowDashboard: Lovelace resource already registered (%s)",
                RESOURCE_URL,
            )
            return

    # Create the new resource
    try:
        await resources.async_create_item(
            {"url": RESOURCE_URL, "res_type": RESOURCE_TYPE}
        )
        _LOGGER.info(
            "EnergyFlowDashboard: registered Lovelace resource %s", RESOURCE_URL
        )
    except Exception as err:  # noqa: BLE001
        _LOGGER.error(
            "EnergyFlowDashboard: failed to register Lovelace resource: %s", err
        )