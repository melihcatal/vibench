from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_openai_client, query_logs
from observability_models import QueryFilters


def main() -> None:
    client = build_openai_client()
    until = datetime.now(timezone.utc)
    since = until - timedelta(hours=2)
    filters = QueryFilters(
        severity="ERROR",
        since_iso=since.isoformat(),
        until_iso=until.isoformat(),
        limit=20,
    )
    query_logs(client, filters)


if __name__ == "__main__":
    main()
