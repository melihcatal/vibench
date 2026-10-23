from pydantic import BaseModel, Field
from typing import Optional

class StructuredLog(BaseModel):
    """

    A Pydantic model for a structured log entry.
    This helps enforce consistency in log payloads across different
    services and application components.

    """
    message: str = Field(description="The main log message.")
    severity: str = Field(default="INFO", description="Log severity (e.g., DEBUG, INFO, WARNING, ERROR).")
    
    # Contextual information
    service_name: Optional[str] = Field(default=None, description="The name of the service or component generating the log.")
    correlation_id: Optional[str] = Field(default=None, description="A unique ID to correlate logs across services for a single request.")
    user_id: Optional[str] = Field(default=None, description="The ID of the user associated with the log event.")
    
    # HTTP Request/Response details
    request_method: Optional[str] = Field(default=None, description="HTTP request method (e.g., GET, POST).")
    request_url: Optional[str] = Field(default=None, description="URL of the HTTP request.")
    response_status_code: Optional[int] = Field(default=None, description="Status code of the HTTP response.")

    class Config:
        # Example for JSON serialization
        json_schema_extra = {
            "example": {
                "message": "User login attempt failed.",
                "severity": "WARNING",
                "service_name": "auth-service",
                "correlation_id": "abc-123-xyz-789",
                "user_id": "user_42",
                "request_method": "POST",
                "request_url": "/api/v1/login",
                "response_status_code": 401
            }
        }
