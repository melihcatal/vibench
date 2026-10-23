from pydantic import BaseModel
from typing import Dict, Any, Optional


class StructuredLogEvent(BaseModel):
    """
    Model for structured log events sent to Datadog.
    """

    timestamp: str
    severity: str
    message: str
    source: str
    attributes: Dict[str, Any]

    def dict(self, **kwargs) -> dict:
        """
        Converts the model to a dictionary for serialization.
        """
        log_dict = super().dict(**kwargs)
        log_dict.update(log_dict.pop("attributes"))
        return {
            "timestamp": log_dict["timestamp"],
            "status": log_dict["severity"],
            "message": log_dict["message"],
            "service": log_dict["source"],
            **{
                k: v
                for k, v in log_dict.items()
                if k not in ["timestamp", "severity", "message", "source"]
            },
        }
