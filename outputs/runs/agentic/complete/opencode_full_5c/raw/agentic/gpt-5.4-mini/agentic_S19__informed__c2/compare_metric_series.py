from datetime import datetime

from observability_client import build_session, load_config
from observability_models import isoformat_utc, parse_datadog_series


def compare_metric_series(metric: str, start: datetime, end: datetime, left_filter: str, right_filter: str):
    config = load_config()
    session = build_session(config)
    params_left = {"from": isoformat_utc(start), "to": isoformat_utc(end), "query": f"avg:{metric}{{{left_filter}}}"}
    params_right = {"from": isoformat_utc(start), "to": isoformat_utc(end), "query": f"avg:{metric}{{{right_filter}}}"}
    left_resp = session.get(f"{config.api_base}/api/v1/query", params=params_left, timeout=config.timeout)
    right_resp = session.get(f"{config.api_base}/api/v1/query", params=params_right, timeout=config.timeout)
    left_resp.raise_for_status()
    right_resp.raise_for_status()
    left_series = parse_datadog_series(left_resp.json())
    right_series = parse_datadog_series(right_resp.json())
    return {"left": left_series, "right": right_series}
