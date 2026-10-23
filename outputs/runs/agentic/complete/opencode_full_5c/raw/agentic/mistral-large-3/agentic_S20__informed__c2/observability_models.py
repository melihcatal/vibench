from typing import Dict, Any, Optional
from datetime import datetime


class LogRequest:
    def __init__(self, severity: str, message: str, **kwargs):
        self.severity = severity
        self.message = message
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.json_payload = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "message": self.message,
            "timestamp": self.timestamp,
            "json_payload": self.json_payload,
        }


class LogResponse:
    def __init__(self, entries: list):
        self.entries = entries

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entries": [
                {
                    "timestamp": entry.get("timestamp", ""),
                    "severity": entry.get("severity", ""),
                    "message": entry.get("message", ""),
                    "json_payload": entry.get("json_payload", {}),
                }
                for entry in self.entries
            ]
        }


class LogNormalizer:
    @staticmethod
    def normalize_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "timestamp": entry.get("timestamp", ""),
            "severity": entry.get("severity", "INFO"),
            "message": entry.get("message", ""),
            "json_payload": entry.get("json_payload", {}),
        }
