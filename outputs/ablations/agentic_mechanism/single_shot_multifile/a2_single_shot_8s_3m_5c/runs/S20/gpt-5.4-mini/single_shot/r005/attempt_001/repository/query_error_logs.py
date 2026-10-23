import json
from datetime import datetime, timedelta, timezone
from observability_client import get_observability_client, resolve_log_namespace
from observability_models import LogQueryRequest


def main():
    client = get_observability_client()
    namespace = resolve_log_namespace()
    request = LogQueryRequest(
        query='severity:"ERROR"',
        start_time=datetime.now(timezone.utc) - timedelta(hours=6),
        end_time=datetime.now(timezone.utc),
        limit=50,
        namespace=namespace,
        filters={"severity": "ERROR"},
    )
    return client.query_logs(request.to_payload())


if __name__ == "__main__":
    print(json.dumps(main(), default=str))