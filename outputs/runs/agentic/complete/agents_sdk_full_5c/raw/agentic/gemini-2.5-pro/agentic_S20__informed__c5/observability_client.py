import os
from google.cloud import logging

def get_logging_client() -> logging.Client:
    """
    Initializes and returns a Google Cloud Logging client.
    Authentication is handled implicitly via GOOGLE_APPLICATION_CREDENTIALS
    environment variable.
    """
    return logging.Client()

def get_logger(name: str = "app_logger"):
    """
    Retrieves a logger instance from the Google Cloud Logging client.
    
    Args:
        name (str): The name of the logger.
        
    Returns:
        A logger instance attached to the default handler.
    """
    client = get_logging_client()
    return client.logger(name)
