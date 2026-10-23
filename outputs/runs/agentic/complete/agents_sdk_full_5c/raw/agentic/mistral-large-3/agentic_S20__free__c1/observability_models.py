from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class StructuredLogEvent(BaseModel):
    """Model for structured log events sent to Datadog."""
    message: str
    timestamp: str
    severity: str = "INFO"
    attributes: Dict[str, Any] = Field(default_factory=dict)

    def dict(self, **kwargs) -> dict:
        """Convert to Datadog-compatible log format."""
        base = super().dict(**kwargs)
        return {
            "message": base["message"],
            "ddsource": "python",
            "ddtags": f"severity:{base['severity']}",
            "timestamp": base["timestamp"],
            **base["attributes"]
        }