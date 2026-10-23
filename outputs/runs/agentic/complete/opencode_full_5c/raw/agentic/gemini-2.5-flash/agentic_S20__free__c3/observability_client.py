import os
from google.cloud import logging
from google.cloud.logging_v2.client import Client as LoggingClient
from google.cloud.logging_v2.entries import LogEntry
from typing import Dict, Any, List, Generator
from observability_models import StructuredLogEntry, CorrelatedLogEntry


class ObservabilityClient:
    def __init__(self, project_id: str = None, log_name: str = "application-logs"):
        if project_id is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if project_id is None:
                raise ValueError(
                    "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set."
                )
        self.project_id = project_id
        self.log_name = log_name
        self.logging_client: LoggingClient = logging.Client(project=self.project_id)

    def write_structured_log(self, entry: StructuredLogEntry):
        logger = self.logging_client.logger(self.log_name)
        log_entry_dict = entry.model_dump(exclude_unset=True, exclude_none=True)

        # Prepare the log entry for Google Cloud Logging
        message = log_entry_dict.pop("message", None)
        severity = log_entry_dict.pop("severity", "INFO")
        timestamp = log_entry_dict.pop("timestamp", None)
        resource_type = log_entry_dict.pop("resource_type", "global")
        resource_labels = log_entry_dict.pop("resource_labels", None)
        json_payload = log_entry_dict.pop("json_payload", None)

        _resource = (
            logging.resource.Resource(type=resource_type, labels=resource_labels)
            if resource_labels
            else None
        )

        if json_payload:
            # If json_payload is provided, it takes precedence for structured data
            logger.log_struct(
                json_payload,
                severity=severity,
                timestamp=timestamp,
                resource=_resource,
                text_payload=message,
            )
        elif log_entry_dict:
            # Otherwise, use the remaining fields as structured data
            logger.log_struct(
                log_entry_dict,
                severity=severity,
                timestamp=timestamp,
                resource=_resource,
                text_payload=message,
            )
        else:
            # Fallback to text payload if no structured data
            logger.log_text(
                message, severity=severity, timestamp=timestamp, resource=_resource
            )

    def write_correlated_log(self, entry: CorrelatedLogEntry):
        logger = self.logging_client.logger(self.log_name)
        log_entry_dict = entry.model_dump(exclude_unset=True, exclude_none=True)

        # Prepare the log entry for Google Cloud Logging
        message = log_entry_dict.pop("message", None)
        severity = log_entry_dict.pop("severity", "INFO")
        timestamp = log_entry_dict.pop("timestamp", None)
        resource_type = log_entry_dict.pop("resource_type", "global")
        resource_labels = log_entry_dict.pop("resource_labels", None)
        json_payload = log_entry_dict.pop("json_payload", None)

        _resource = (
            logging.resource.Resource(type=resource_type, labels=resource_labels)
            if resource_labels
            else None
        )

        # Ensure correlation_id is part of json_payload or top-level if possible
        if json_payload is None:
            json_payload = {}
        if "correlation_id" not in json_payload and "correlation_id" in log_entry_dict:
            json_payload["correlation_id"] = log_entry_dict.pop("correlation_id")

        # Add any remaining fields to json_payload if they exist and are not already there
        for key, value in log_entry_dict.items():
            if key not in json_payload:
                json_payload[key] = value

        logger.log_struct(
            json_payload,
            severity=severity,
            timestamp=timestamp,
            resource=_resource,
            text_payload=message,
        )

    def query_logs(
        self, filter_string: str, order_by: str = "timestamp desc", limit: int = 100
    ) -> Generator[LogEntry, None, None]:
        return self.logging_client.list_entries(
            filter_=filter_string, order_by=order_by, page_size=limit
        )
