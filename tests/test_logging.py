"""Test the startup log observer with Python's actual logging API."""

import inspect
import logging
import unittest
from unittest.mock import Mock, patch

from custom_components.start_time.sensor import StartTime


class LoggingObserverTests(unittest.TestCase):
    """Preserve log records and observe only valid initialization messages."""

    def setUp(self):
        """Capture bootstrap records without retaining a patched global logger."""
        self.logger = logging.getLogger("homeassistant.bootstrap")
        previous_info = self.logger.info
        previous_level = self.logger.level
        self.addCleanup(setattr, self.logger, "info", previous_info)
        self.addCleanup(self.logger.setLevel, previous_level)
        self.logger.setLevel(logging.INFO)
        self.records = []
        handler = logging.Handler()
        handler.emit = self.records.append
        self.logger.addHandler(handler)
        self.addCleanup(self.logger.removeHandler, handler)
        self.sensor = StartTime()
        self.sensor.internal_update = Mock()

    def test_standard_logging_keywords_and_caller(self):
        """Pass log metadata through and preserve the original caller."""
        try:
            raise ValueError("synthetic error")
        except ValueError:
            line = inspect.currentframe().f_lineno + 1
            self.logger.info(
                "Initialization pending",
                extra={"test_marker": True},
                exc_info=True,
                stack_info=True,
            )

        record = self.records[-1]
        self.assertTrue(record.test_marker)
        self.assertIs(record.exc_info[0], ValueError)
        self.assertTrue(record.stack_info)
        self.assertEqual(record.funcName, "test_standard_logging_keywords_and_caller")
        self.assertEqual(record.lineno, line)
        self.sensor.internal_update.assert_not_called()

    def test_explicit_stacklevel(self):
        """Caller-selected stack depth must still skip the observer wrapper."""

        def log_from_helper():
            self.logger.info("Initialization pending", stacklevel=2)

        log_from_helper()
        self.assertEqual(self.records[-1].funcName, "test_explicit_stacklevel")

    def test_startup_duration_observed(self):
        """Observe the original format string while retaining its record."""
        self.logger.info("Home Assistant initialized in %.2fs", 12.345)
        self.sensor.internal_update.assert_called_once_with(12.345)
        self.assertEqual(
            self.records[-1].getMessage(), "Home Assistant initialized in 12.35s"
        )

    def test_non_string_message_and_missing_arguments(self):
        """Python logging accepts arbitrary message objects and literal strings."""
        with patch("custom_components.start_time.sensor._LOGGER.warning") as warning:
            self.logger.info({"status": "starting"})
            self.logger.info("Home Assistant initialized")
        warning.assert_not_called()
        self.sensor.internal_update.assert_not_called()
        self.assertEqual(len(self.records), 2)


if __name__ == "__main__":
    unittest.main()
