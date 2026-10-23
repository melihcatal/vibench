from datetime import datetime

from observability_client import build_session, load_config
from observability_models import MetricWindowRequest, isoformat_utc, normalize_tags


def aggregate_metric_stats(metric: str, start: datetime, end: datetime, tags=None):
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
    data = resp.json()
    series = data.get("series", [])
    values = [p[1] for s in series for p in s.get("pointlist", []) if p and len(p) > 1 and p[1] is not None]
    return {
        "metric": metric,
        "start": req.start,
        "end": req.end,
        "count": len(values),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "avg": (sum(values) / len(values)) if values else None,
        "sum": sum(values) if values else None,
    }
