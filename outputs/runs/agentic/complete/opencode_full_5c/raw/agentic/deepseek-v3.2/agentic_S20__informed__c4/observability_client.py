import os
import json
from typing import Optional, Dict, Any
from google.cloud import logging
from google.auth.exceptions import DefaultCredentialsError


class ObservabilityClient:
    """Client helper utilities for Google Cloud Logging integration."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self._client = None
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize the Google Cloud Logging client."""
        try:
            if not self.project_id:
                self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
                if not self.project_id:
                    print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set")

            self._client = logging.Client(project=self.project_id)
            self._initialized = True
            print(
                f"Google Cloud Logging client initialized for project: {self.project_id}"
            )
            return True
        except DefaultCredentialsError as e:
            print(f"Failed to initialize Google Cloud Logging client: {e}")
            print(
                "Ensure GOOGLE_APPLICATION_CREDENTIALS is set or running in GCP environment"
            )
            return False
        except Exception as e:
            print(f"Unexpected error initializing client: {e}")
            return False

    @property
    def client(self) -> logging.Client:
        """Get the Google Cloud Logging client instance."""
        if not self._initialized:
            self.initialize()
        return self._client

    def get_logger(self, logger_name: str) -> Any:
        """Get a logger instance for the specified name."""
        if not self._initialized:
            self.initialize()
        return self._client.logger(logger_name)

    def validate_log_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize log payload structure."""
        validated = payload.copy()

        # Ensure required fields
        if "message" not in validated:
            validated["message"] = "No message provided"

        if "severity" not in validated:
            validated["severity"] = "INFO"

        # Add metadata
        validated["_metadata"] = {
            "source": "observability_client",
            "timestamp": os.getenv("LOG_TIMESTAMP", ""),
            "version": "1.0.0",
        }

        return validated

    def format_log_entry(self, severity: str, message: str, **kwargs) -> Dict[str, Any]:
        """Format a standardized log entry."""
        entry = {
            "severity": severity.upper(),
            "message": message,
            "service": kwargs.get("service", os.getenv("SERVICE_NAME", "unknown")),
            "environment": kwargs.get(
                "environment", os.getenv("ENVIRONMENT", "development")
            ),
            "timestamp": kwargs.get("timestamp", ""),
        }

        # Add any additional fields
        for key, value in kwargs.items():
            if key not in [
                "severity",
                "message",
                "service",
                "environment",
                "timestamp",
            ]:
                entry[key] = value

        return entry

    def get_default_labels(self) -> Dict[str, str]:
        """Get default labels for log entries."""
        return {
            "environment": os.getenv("ENVIRONMENT", "development"),
            "service": os.getenv("SERVICE_NAME", "unknown"),
            "version": os.getenv("SERVICE_VERSION", "1.0.0"),
        }
