import logging
from playwright.sync_api import sync_playwright
import pytest
import os

# Custom log level for tracking steps
STEP_LOG_LEVEL = logging.INFO + 5
logging.addLevelName(STEP_LOG_LEVEL, "STEP")

def log_step(message, *args, **kwargs):
    logging.log(STEP_LOG_LEVEL, message, *args, **kwargs)

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(STEP_LOG_LEVEL)

    # Delete previous log file if it exists
    log_file_path = 'test_log.txt'
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    # File handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(STEP_LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter('%(message)s'))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(STEP_LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter('%(message)s'))

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Configure logging
setup_logger()


