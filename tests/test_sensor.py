"""Test the native duration sensor and existing setup-time attributes."""

import logging
import unittest
from datetime import timedelta
from unittest.mock import Mock

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant

from custom_components.start_time.sensor import DOMAIN, StartTime


class DurationSensorTests(unittest.TestCase):
    """Keep entity identity and setup details when exposing a native duration."""

    def setUp(self):
        """Isolate the bootstrap observer and state scheduling."""
        logger = logging.getLogger("homeassistant.bootstrap")
        previous_info = logger.info
        self.addCleanup(setattr, logger, "info", previous_info)
        self.sensor = StartTime()
        self.sensor.hass = Mock(spec=HomeAssistant)
        self.sensor.hass.data = {}
        self.sensor.schedule_update_ha_state = Mock()

    def test_native_duration_and_identity(self):
        """Expose numeric seconds using Home Assistant's duration metadata."""
        self.assertIsInstance(self.sensor, SensorEntity)
        self.assertIsNone(self.sensor.native_value)
        self.assertEqual(self.sensor.device_class, SensorDeviceClass.DURATION)
        self.assertEqual(self.sensor.native_unit_of_measurement, UnitOfTime.SECONDS)
        self.assertEqual(self.sensor.unique_id, DOMAIN)
        self.assertEqual(self.sensor.name, "Start Time")
        self.assertFalse(self.sensor.should_poll)

        self.sensor.internal_update(12.345)
        self.assertEqual(self.sensor.native_value, 12.35)
        self.sensor.schedule_update_ha_state.assert_called_once_with()

    def test_legacy_setup_time_values_preserved(self):
        """Retain float and timedelta attributes without mutating core data."""
        setup = {"fast": 0.1234, "slow": timedelta(seconds=2.345), "ignored": None}
        self.sensor.hass.data["setup_time"] = setup
        self.sensor.internal_update(3.456)
        self.assertEqual(
            self.sensor.extra_state_attributes, {"slow": 2.35, "fast": 0.12}
        )
        self.assertEqual(list(self.sensor.extra_state_attributes), ["slow", "fast"])
        self.assertIsNone(setup["ignored"])
        self.assertEqual(setup["fast"], 0.1234)

    def test_nested_setup_time_values_preserved(self):
        """Retain setup-time aggregation used since Home Assistant 2024.4."""
        setup = {"example": {"setup": {"domain": 0.25}, "entry": {"entry": 0.5}}}
        self.sensor.hass.data["setup_time"] = setup
        self.sensor.internal_update(1.25)
        self.assertEqual(self.sensor.native_value, 1.25)
        self.assertEqual(self.sensor.extra_state_attributes, {"example": 0.75})
        self.assertEqual(setup["example"]["entry"]["entry"], 0.5)


if __name__ == "__main__":
    unittest.main()
