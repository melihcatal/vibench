from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import datetime

class StructuredLog(BaseModel):
    """
    A Pydantic model for a structured log event.
    """
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    message: str
    service: str = "default-service"
    hostname: str = "local-dev"
    level: str = "INFO"
    ddsource: str = "python"
    ddtags: str = "env:dev"
    extra_attributes: Dict[str, Any] = Field(default_factory=dict)

    def to_datadog_payload(self) -> Dict[str, Any]:
        """Converts the model to a dictionary suitable for Datadog API."""
        payload = self.model_dump(exclude={"extra_attributes", "level"})
        payload.update(self.extra_attributes)
        payload["timestamp"] = self.timestamp.isoformat()
        payload["status"] = self.level
        return payload

class LogQueryResponse(BaseModel):
    """
    Represents a simplified log entry from a query response.
    """
    id: str
    timestamp: datetime.datetime
    message: str
    attributes: Dict[str, Any]

class LogQueryFilter(BaseModel):
    """

    Represents filters for querying logs.
    """
    query: str
    from_time: str = "now-15m"
    to_time: str = "now"
    limit: int = 100
