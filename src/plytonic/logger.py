import logging
from logging import Formatter, getLogger, StreamHandler


class Logger:

    def __init__(self):
        self.formatter = Formatter("%(asctime)s %(levelname)s: %(message)s")
        self.handler = StreamHandler()
        self.handler.setFormatter(self.formatter)
        self.logger = getLogger("plytonic")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)


LOGGER = Logger()


if __name__ == "__main__":

    LOGGER.info("started")
    LOGGER.warn("and reached this point!")