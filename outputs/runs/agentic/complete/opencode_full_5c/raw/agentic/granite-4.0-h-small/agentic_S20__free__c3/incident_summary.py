import json
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import normalize_batch

client = ObservabilityClient()


def summarize_errors(service: str, start_relative: int = 3600):
    """Summarize recent error logs for incident review."""
    errors = client.query_logs(
        query=f"service:{service} severity:error",
        start=int(
            (datetime.utcnow() - timedelta(seconds=start_relative)).timestamp() * 1000
        ),
        end=int(datetime.utcnow().timestamp() * 1000),
    )
    normalized = normalize_batch(errors)
    summary = {
        "service": service,
        "time_window_seconds": start_relative,
        "total_errors": len(normalized),
        "first_error_timestamp": normalized[0].timestamp if normalized else None,
        "last_error_timestamp": normalized[-1].timestamp if normalized else None,
        "sample_errors": [e.message for e in normalized[:5]],
    }
    return json.dumps(summary, indent=2)


# Example (removed)
# print(summarize_errors(service="order-service"))
