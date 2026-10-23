from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_openai_client, query_logs
from observability_models import QueryFilters


def main() -> None:
    client = build_openai_client()
    until = datetime.now(timezone.utc)
    since = until - timedelta(minutes=30)
    filters = QueryFilters(
        field_name="service",
        field_value="checkout-api",
        since_iso=since.isoformat(),
        until_iso=until.isoformat(),
        limit=50,
    )
    query_logs(client, filters)


if __name__ == "__main__":
    main()
