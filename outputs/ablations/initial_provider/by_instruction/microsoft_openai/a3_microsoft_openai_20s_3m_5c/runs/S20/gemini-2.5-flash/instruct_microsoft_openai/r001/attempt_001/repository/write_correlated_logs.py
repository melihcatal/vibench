import logging
import uuid
import datetime
import os
from observability_client import observability_client
from observability_models import CorrelatedLogEvent

# Get a logger and attach the OpenTelemetry handler
logger = logging.getLogger(__name__)
logger.addHandler(observability_client.handler)
logger.setLevel(logging.INFO)

def write_correlated_logs(session_id: str):
    correlation_id = str(uuid.uuid4())
    
    # Simulate a series of correlated log events
    log_events_data = [
        {"message": "User session started.", "level": "info", "user_id": session_id},
        {"message": "Data fetched from service X.", "level": "info", "service_name": "ServiceX", "duration_ms": 150},
        {"message": "Processing complete for request.", "level": "info"},
        {"message": "Potential error in user data processing.", "level": "warning", "user_id": session_id, "error_code": "E401"}
    ]

    for i, event_data in enumerate(log_events_data):
        message = event_data["message"]
        level = event_data["level"]
        properties = {k: v for k, v in event_data.items() if k not in ["message", "level"]}
        
        # Create CorrelatedLogEvent
        correlated_event = CorrelatedLogEvent(
            message=message,
            correlation_id=correlation_id,
            level=level,
            timestamp=datetime.datetime.utcnow().isoformat() + "Z",
            step=i+1,
            **properties
        )

        # Ingest the log using the OpenTelemetry-configured logger
        # The correlation_id and other properties will be attached as attributes/custom dimensions
        extra_properties = {"custom_dimensions": {"correlation_id": correlation_id, **properties}}
        
        if level == "info":
            logger.info(correlated_event.message, extra=extra_properties)
        elif level == "warning":
            logger.warning(correlated_event.message, extra=extra_properties)
        elif level == "error":
            logger.error(correlated_event.message, extra=extra_properties)
        else:
            logger.debug(correlated_event.message, extra=extra_properties)
            
        print(f"Ingested Correlated Log (Correlation ID: {correlation_id}): {correlated_event.to_json()}")

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     write_correlated_logs("user_session_abc")
