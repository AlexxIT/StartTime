from homeassistant.config_entries import ConfigEntry, SOURCE_IMPORT
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .sensor import DOMAIN, StartTime

async def async_setup(hass: HomeAssistant, hass_config: dict):
    """Set up the Start Time component."""
    hass.data[DOMAIN] = StartTime()

    if DOMAIN in hass_config and not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}
        ))
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Start Time from a config entry."""
    await hass.config_entries.async_forward_entry_setups(config_entry, [Platform.SENSOR])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR])
