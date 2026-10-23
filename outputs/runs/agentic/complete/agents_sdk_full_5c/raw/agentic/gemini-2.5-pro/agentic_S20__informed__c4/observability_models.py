from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class StructuredLog(BaseModel):
    """
    Represents a structured log entry for application logging.
    """
    message: str
    severity: str = Field(default="INFO", description="Log severity level (e.g., INFO, ERROR, WARNING)")
    service_name: str = Field(description="Name of the service generating the log")
    correlation_id: Optional[str] = Field(default=None, description="Identifier to correlate logs across services")
    additional_data: Optional[Dict[str, Any]] = Field(default=None, description="Any other structured data")

