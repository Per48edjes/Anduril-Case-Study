import logging
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUERIES_DIR = os.path.join(PROJECT_ROOT, "queries")
PROFILES_DIR = os.path.join(PROJECT_ROOT, "profiles")
TRANSFORMATIONS_DIR = os.path.join(PROJECT_ROOT, "transformations")
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "artifacts")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")


def setup_logging(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    file_handler = logging.FileHandler(
        os.path.join(LOGS_DIR, f"{name}:{timestamp}.log")
    )
    console_handler = logging.StreamHandler()

    for handler in [file_handler, console_handler]:
        handler.setLevel(logging.DEBUG if handler == file_handler else logging.ERROR)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
