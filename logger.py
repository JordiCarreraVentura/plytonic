import logging


class PlytonicLogger:

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s',
            level=logging.DEBUG
        )
    
    def warn(self, message: str) -> None:
        logging.warn(message)
    
    def __call__(self, message: str) -> None:
        logging.info(message)


LOGGER = PlytonicLogger()