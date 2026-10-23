from collections import Counter
from observability_client import get_logs_client, resolve_log_name
from observability_models import build_query_request
from datetime import datetime, timedelta, timezone


def main():
    client = get_logs_client()
    log_name = resolve_log_name()
    request = build_query_request(
        log_name=log_name,
        severity="ERROR",
        start_time=datetime.now(timezone.utc) - timedelta(days=1),
        end_time=datetime.now(timezone.utc),
        field_filters={"severity": "ERROR"},
    )
    result = client.query_error_logs(request)
    counts = Counter(entry.get("message", "") for entry in result.entries)
    summary = {"total_errors": len(result.entries), "top_messages": counts.most_common(5)}
    return summary


if __name__ == "__main__":
    main()
