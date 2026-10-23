from datetime import datetime, timedelta, timezone
from observability_client import datadog_api_base, datadog_headers, load_datadog_config, get_json
from observability_models import LogQueryResult, normalize_log_items


def main() -> LogQueryResult:
    config = load_datadog_config()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    params = {
        "filter[query]": f"service:{config.service} source:{config.source}",
        "filter[from]": start.isoformat().replace("+00:00", "Z"),
        "filter[to]": end.isoformat().replace("+00:00", "Z"),
        "page[limit]": 50,
    }
    payload = get_json(f"{datadog_api_base(config)}/api/v2/logs/events/search", datadog_headers(config), params=params)
    items = normalize_log_items(payload)
    return LogQueryResult(items=items, total=payload.get("meta", {}).get("page", {}).get("total", len(items)))


if __name__ == "__main__":
    print(main())
