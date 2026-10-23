from google.cloud import logging
from google.api_core.exceptions import GoogleAPICallError
import os
from typing import Optional


class ObservabilityClient:
    """
    Client helper utilities for Google Cloud Logging.
    """

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initializes the Google Cloud Logging client.

        Args:
            credentials_path (str, optional): Path to the service account JSON file.
                                           Defaults to GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if credentials_path:
            self.client = logging.Client.from_service_account_json(credentials_path)
        else:
            self.client = logging.Client.from_service_account_json(
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            )

    def get_logger(self, log_name: str) -> logging.Logger:
        """
        Gets a logger instance for the specified log name.

        Args:
            log_name (str): The name of the log.

        Returns:
            logging.Logger: The logger instance.
        """
        return self.client.logger(log_name)

    def validate_log_structure(self, log_data: dict) -> bool:
        """
        Validates the structure of a log entry.

        Args:
            log_data (dict): The log data to validate.

        Returns:
            bool: True if the log data is valid, False otherwise.
        """
        if not isinstance(log_data, dict):
            return False
        return True
