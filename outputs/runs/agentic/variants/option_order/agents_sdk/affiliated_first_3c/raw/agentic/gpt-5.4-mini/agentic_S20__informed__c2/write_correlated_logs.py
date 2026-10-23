from datetime import datetime, timezone
from uuid import uuid4

from observability_client import ingest_log
from observability_models import LogEvent

DATADOG_LOG_SERVICE = "correlated-log-writer"


def write_correlated_logs(user_message: str, operations: list[str] | None = None) -> dict:
    correlation_id = str(uuid4())
    operations = operations or ["start", "process", "finish"]
    results = []
    for index, operation in enumerate(operations):
        event = LogEvent(
            message=f"{user_message} :: {operation}",
            service=DATADOG_LOG_SERVICE,
            severity="info",
            timestamp=datetime.now(timezone.utc),
            correlation_id=correlation_id,
            request_id=f"req-{index}",
            fields={"operation": operation, "sequence": index},
        )
        results.append(ingest_log(event))
    return {"correlation_id": correlation_id, "results": results}
