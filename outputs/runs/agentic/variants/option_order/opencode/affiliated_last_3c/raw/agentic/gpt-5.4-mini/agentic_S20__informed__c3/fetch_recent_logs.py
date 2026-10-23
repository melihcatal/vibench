from datetime import datetime, timedelta, timezone

from observability_client import (
    datadog_headers,
    datadog_query_url,
    load_config,
    get_json,
)
from observability_models import build_search_params, parse_log_hits


def main() -> None:
    config = load_config()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    query = f"service:{config.service} source:{config.source} env:production"
    payload = get_json(
        datadog_query_url(config.site),
        datadog_headers(config),
        build_search_params(query, start.isoformat(), end.isoformat(), limit=25),
    )
    parse_log_hits(payload)


if __name__ == "__main__":
    main()
