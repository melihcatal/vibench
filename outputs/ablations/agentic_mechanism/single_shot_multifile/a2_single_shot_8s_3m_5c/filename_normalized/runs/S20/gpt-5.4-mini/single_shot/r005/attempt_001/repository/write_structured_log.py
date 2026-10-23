import os
import json
import uuid
from datetime import datetime, timezone
from observability_client import get_observability_client, resolve_log_namespace, resolve_log_source
from observability_models import StructuredLogEvent, normalize_dict_payload


def main():
    client = get_observability_client()
    namespace = resolve_log_namespace()
    source = resolve_log_source("structured-log-writer")
    event = StructuredLogEvent(
        message="structured event written",
        severity="INFO",
        service="app-api",
        source=source,
        correlation_id=str(uuid.uuid4()),
        fields=normalize_dict_payload({"action": "write_structured_log", "status": "ok"}),
        timestamp=datetime.now(timezone.utc),
    )
    return client.write_log(event.to_payload(namespace=namespace))


if __name__ == "__main__":
    print(json.dumps(main(), default=str))