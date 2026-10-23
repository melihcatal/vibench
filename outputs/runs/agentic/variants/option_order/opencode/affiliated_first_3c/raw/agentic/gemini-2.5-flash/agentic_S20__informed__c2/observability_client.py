import os
from google.cloud import logging_v2
from google.cloud.logging_v2.client import Client as LoggingClient
from google.cloud.logging_v2.logger import Logger as LoggingLogger


def get_logging_client() -> LoggingClient:
    """Initializes and returns a Google Cloud Logging client."""
    return logging_v2.Client()


def get_logger(log_name: str) -> LoggingLogger:
    """Initializes and returns a Google Cloud Logging logger."""
    client = get_logging_client()
    return client.logger(log_name)
