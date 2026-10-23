import datetime
import json
from observability_client import ObservabilityClient
from observability_models import StructuredLogEvent

def write_structured_log(message: str, severity: str, service_name: str, **kwargs):
    client = ObservabilityClient()
    
    if client.openai_client is None:
        print("Warning: Azure OpenAI client not initialized in ObservabilityClient. Ensure AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are set.")

    log_event = StructuredLogEvent(
        message=message,
        severity=severity,
        service_name=service_name,
        event_timestamp=datetime.datetime.utcnow().isoformat(),
        **kwargs
    )
    
    log_type = "MyApplicationLogs"
    
    try:
        client.post_log_event(log_type, [log_event.to_json()])
    except Exception as e:
        print(f"Error writing structured log: {e}")