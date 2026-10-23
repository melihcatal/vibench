import json
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry
from opentelemetry import trace

def write_structured_log(log_entry: LogEntry):
    client = ObservabilityClient()
    tracer = client.get_tracer()

    if not tracer:
        print(f"Azure Monitor tracer not configured. Log entry not sent: {log_entry.to_json()}")
        return

    with tracer.start_as_current_span(f"write_log_{log_entry.severity.lower()}") as span:
        span.set_attribute("log.message", log_entry.message)
        span.set_attribute("log.severity", log_entry.severity)
        span.set_attribute("log.timestamp", log_entry.timestamp.isoformat())

        for key, value in log_entry.properties.items():
            span.set_attribute(f"log.properties.{key}", json.dumps(value) if isinstance(value, (dict, list)) else value)
        
        # In OpenTelemetry, custom structured logs are often represented as attributes on a span
        # For richer integration with Azure Monitor's custom logs, one might use a direct API or a custom exporter
        # This example uses span attributes which will be visible in Application Insights traces
        print(f"Structured log sent to Azure Monitor: {log_entry.to_json()}")

if __name__ == "__main__":
    # Example usage:
    log = LogEntry(
        message="User login failed",
        severity="ERROR",
        timestamp=datetime.utcnow(),
        properties={
            "user_id": "user123",
            "ip_address": "192.168.1.1",
            "reason": "Invalid password"
        }
    )
    write_structured_log(log)

    log_info = LogEntry(
        message="User viewed product page",
        severity="INFO",
        timestamp=datetime.utcnow(),
        properties={
            "user_id": "user456",
            "product_id": "prod789"
        }
    )
    write_structured_log(log_info)
