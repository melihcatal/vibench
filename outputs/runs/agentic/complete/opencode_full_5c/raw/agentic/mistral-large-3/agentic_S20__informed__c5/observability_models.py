from typing import Dict, Any, Optional
from datetime import datetime


class LogEntry:
    """
    Represents a standardized log entry for Google Cloud Logging.
    """

    def __init__(
        self,
        message: str,
        severity: str = "INFO",
        timestamp: Optional[str] = None,
        **kwargs,
    ):
        """
        Initializes a log entry.

        Args:
            message (str): The log message.
            severity (str): The severity level (e.g., INFO, ERROR, WARNING).
            timestamp (str, optional): The timestamp in ISO format. Defaults to current time.
            **kwargs: Additional log fields.
        """
        self.message = message
        self.severity = severity
        self.timestamp = timestamp if timestamp else datetime.utcnow().isoformat()
        self.additional_fields = kwargs

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the log entry to a dictionary.

        Returns:
            Dict[str, Any]: The log entry as a dictionary.
        """
        log_dict = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }
        log_dict.update(self.additional_fields)
        return log_dict


class LogQueryResponse:
    """
    Represents a standardized response for log queries.
    """

    def __init__(self, entries: list[dict]):
        """
        Initializes a log query response.

        Args:
            entries (list[dict]): List of log entries.
        """
        self.entries = entries

    def normalize(self) -> list[dict]:
        """
        Normalizes log entries to a consistent format.

        Returns:
            list[dict]: List of normalized log entries.
        """
        normalized_entries = []
        for entry in self.entries:
            normalized_entry = {
                "timestamp": entry.get("timestamp", ""),
                "severity": entry.get("severity", "INFO"),
                "message": entry.get("payload", {}).get("message", ""),
                "payload": entry.get("payload", {}),
            }
            normalized_entries.append(normalized_entry)
        return normalized_entries
