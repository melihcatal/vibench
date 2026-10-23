import os, json
import uuid
from datetime import datetime
from typing import Dict, Any
from observability_client import ObservabilityClient

SUPPORTED_REGION = os.getenv('SERVICE_REGION')

# Placeholder for a managed logging service SDK (e.g., Datadog, Splunk, Elastic)
# Replace the dummy client with the real provider SDK in production.
class ManagedLogClient:
    def __init__(self):
        # Configuration loaded from environment or config file
        self.region = SUPPORTED_REGION
    
    def write(self, event_name: str, payload: Dict[str, Any]) -> None:
        # Example call to provider SDK; actual implementation will use provider's `write`/`post` method.
        # Here we simply print to simulate sending the log to the managed service.
        print(f"[WRITE LOG] {event_name} @ {self.region} -> {payload}")

# Singleton instance
log_client = ManagedLogClient()

def write_structured_log(event_name: str, payload: Dict[str, Any], timestamp: str = None) -> None:
    """
    Write a single structured JSON log event to the managed logging service.
    A unique `correlation_id` is automatically added if not supplied.
    """
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()
    payload = {
        "timestamp": timestamp,
        "level": payload.get("level", "INFO"),
        "service": payload.get("service", "unknown-service"),
        "message": payload.get("message", "no message"),
        "correlation_id": payload.get("correlation_id", str(uuid.uuid4())),
        **payload  # include any extra fields
    }
    log_client.write(event_name, payload)
