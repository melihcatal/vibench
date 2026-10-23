from datetime import datetime
from typing import List

from observability_client import build_session, load_config
from observability_models import isoformat_utc, normalize_tags, parse_datadog_series


def filter_metric_dimensions(metric: str, start: datetime, end: datetime, dimensions: List[str] | None = None):
    config = load_config()
    session = build_session(config)
    dims = normalize_tags(dimensions)
    params = {
        "from": isoformat_utc(start),
        "to": isoformat_utc(end),
        "query": f"avg:{metric}{{{','.join(dims)}}}",
    }
    resp = session.get(f"{config.api_base}/api/v1/query", params=params, timeout=config.timeout)
    resp.raise_for_status()
    return parse_datadog_series(resp.json())
