import json
from datetime import datetime, timedelta, timezone
from observability_client import get_log_client, resolve_log_source
from observability_models import LogQuery, normalize_query_result


def main() -> dict:
    client = get_log_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=6)
    query = LogQuery(
        severity="ERROR",
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        source=resolve_log_source("error-query"),
        limit=50,
    )
    result = client.query_logs(query)
    return normalize_query_result(result)


if __name__ == "__main__":
    print(json.dumps(main()))
