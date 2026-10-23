from datetime import datetime
from typing import List

from observability_client import build_session, load_config
from observability_models import MetricWindowRequest, isoformat_utc, normalize_tags, parse_datadog_series


def query_metric_window(metric: str, start: datetime, end: datetime, tags: List[str] | None = None):
    config = load_config()
    session = build_session(config)
    req = MetricWindowRequest(metric=metric, start=start, end=end, tags=normalize_tags(tags))
    params = {
        "from": isoformat_utc(req.start),
        "to": isoformat_utc(req.end),
        "query": f"{req.aggregator}:{req.metric}{{{','.join(req.tags or [])}}}",
    }
    resp = session.get(f"{config.api_base}/api/v1/query", params=params, timeout=config.timeout)
    resp.raise_for_status()
    return parse_datadog_series(resp.json())
