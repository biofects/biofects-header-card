"""Biofects Header Card Component."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.discovery import load_platform

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Biofects Header Card component."""
    
    # Setup sensor platform
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform(
            'sensor', DOMAIN, {}, config
        )
    )
    
    return True
