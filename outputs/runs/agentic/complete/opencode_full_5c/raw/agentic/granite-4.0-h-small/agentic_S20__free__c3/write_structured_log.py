import json
from datetime import datetime, timedelta


def write_structured_log(
    service: str, message: str, severity: str, correlation_id: str = None
):
    """Write a single structured JSON log event to Datadog log ingestion endpoint.
    Uses Datadog Logs API (https://docs.datadoghq.com/logs/log_collection/http_endpoint/?tab=python).
    """
    log_event = {
        "service": service,
        "message": message,
        "ddsource": service,
        "severity": severity,
    }
    if correlation_id:
        log_event["correlation_id"] = correlation_id
    # Convert to JSON string
    payload = json.dumps(log_event)
    # In a real implementation you would POST this payload to Datadog
    # e.g., requests.post('https://http-intake.logs.datadoghq.com/v1/input', headers={'DD-API-KEY': DD_API_KEY}, data=payload)
    print(f"[WRITE] Structured log payload: {payload}")


# Example usage (removed in final file)
# write_structured_log(service="my-app", message="User login succeeded", severity="info", correlation_id="req-12345")
