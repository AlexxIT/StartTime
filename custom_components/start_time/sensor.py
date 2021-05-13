from homeassistant.helpers.entity import Entity

from . import DOMAIN, handler


async def async_setup_entry(hass, entry, async_add_entities):
    handler.sensor = StartTime()
    handler.update()

    async_add_entities([handler.sensor])


class StartTime(Entity):
    _state = None
    _attrs = None

    @property
    def should_poll(self):
        return False

    @property
    def unique_id(self):
        return DOMAIN

    @property
    def name(self):
        return "Start Time"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs

    @property
    def unit_of_measurement(self):
        return 'seconds'

    @property
    def icon(self):
        return 'mdi:home-assistant'

    def update(self, state, attrs):
        self._state = state
        self._attrs = attrs
        self.schedule_update_ha_state()
