import json
import uuid
from datetime import datetime, timezone
from observability_client import get_observability_client, resolve_log_namespace, resolve_log_source
from observability_models import StructuredLogEvent, normalize_dict_payload


def main():
    client = get_observability_client()
    namespace = resolve_log_namespace()
    source = resolve_log_source("correlated-log-writer")
    correlation_id = str(uuid.uuid4())
    events = [
        StructuredLogEvent(
            message="request started",
            severity="INFO",
            service="checkout-service",
            source=source,
            correlation_id=correlation_id,
            fields=normalize_dict_payload({"step": "start", "endpoint": "/checkout"}),
            timestamp=datetime.now(timezone.utc),
        ),
        StructuredLogEvent(
            message="request completed",
            severity="INFO",
            service="checkout-service",
            source=source,
            correlation_id=correlation_id,
            fields=normalize_dict_payload({"step": "complete", "duration_ms": 143}),
            timestamp=datetime.now(timezone.utc),
        ),
    ]
    return [client.write_log(event.to_payload(namespace=namespace)) for event in events]


if __name__ == "__main__":
    print(json.dumps(main(), default=str))