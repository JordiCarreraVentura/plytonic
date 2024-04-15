import logging


class PlytonicLogger:

    def __init__(self):
        self.logger = logging.getLogger('plytonic')
        self.logger.setLevel(logging.DEBUG)
        # logging.basicConfig(
        #     format='%(asctime)s %(levelname)s: %(message)s',
        #     level=logging.DEBUG
        # )
    
    def warn(self, message: str) -> None:
        self.logger.warn(message)
    
    def __call__(self, message: str) -> None:
        self.logger.info(message)


LOGGER = PlytonicLogger()