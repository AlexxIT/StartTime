import logging
from collections import OrderedDict


class LogsHandler:
    state = None
    attrs = {}
    sensor = None

    def add_logger(self, name: str):
        logger = logging.getLogger(name)
        real_info = logger.info

        def monkey_info(msg: str, *args):
            if msg.startswith("Setup of domain"):
                self.attrs[args[0]] = round(args[1], 1)

            elif msg.startswith("Home Assistant initialized"):
                self.state = round(args[0], 1)
                at = sorted(self.attrs.items(), key=lambda t: t[1],
                            reverse=True)
                self.attrs = OrderedDict(at)
                self.update()

            real_info(msg, *args)

        logger.info = monkey_info

    def update(self):
        if self.state and self.sensor:
            self.sensor.update(self.state, self.attrs)
