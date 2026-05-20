import logging
import sys


def get_logger(name: str = "datavenir"):
    """
    Crée un logger standard pour tout le projet.
    """

    logger = logging.getLogger(name)

    # évite les doubles logs
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger