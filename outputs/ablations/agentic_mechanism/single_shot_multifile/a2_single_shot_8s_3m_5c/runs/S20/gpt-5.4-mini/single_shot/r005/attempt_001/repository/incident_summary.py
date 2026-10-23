import json
from datetime import datetime, timedelta, timezone
from observability_client import get_observability_client, resolve_log_namespace
from observability_models import LogQueryRequest


def main():
    client = get_observability_client()
    namespace = resolve_log_namespace()
    request = LogQueryRequest(
        query='severity:"ERROR"',
        start_time=datetime.now(timezone.utc) - timedelta(hours=24),
        end_time=datetime.now(timezone.utc),
        limit=100,
        namespace=namespace,
        filters={"service": "checkout-service"},
    )
    results = client.query_logs(request.to_payload())
    entries = results.get("results", []) if isinstance(results, dict) else results
    error_count = len(entries)
    services = sorted({item.get("service", "unknown") for item in entries if isinstance(item, dict)})
    summary = {
        "error_count": error_count,
        "services": services,
        "window_hours": 24,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    return summary


if __name__ == "__main__":
    print(json.dumps(main(), default=str))