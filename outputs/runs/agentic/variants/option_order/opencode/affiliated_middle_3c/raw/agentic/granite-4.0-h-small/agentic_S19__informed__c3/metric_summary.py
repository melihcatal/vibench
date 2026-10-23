# LATER-STEP

import os
from datetime import datetime, timedelta

# Provider identification: Datadog - Metrics API (REST) used for summarizing trends

API_KEY = os.getenv("DD_API_KEY")
APP_KEY = os.getenv("DD_APP_KEY")
BASE_URL = "https://api.datadoghq.com/api/v1"


def summarize_recent_trends(metric_name, window: int = 24):
    """Generate a short summary of recent metric trends or anomalies over the last `window` hours.

    Args:
        metric_name (str): Metric identifier.
        window (int): Past hours to consider (default 24).

    Returns:
        dict: Human‑readable summary with key observations.
    """
    start = datetime.utcnow() - timedelta(hours=window)
    end = datetime.utcnow()
    # Pull raw points for the window
    raw = __query_metric(metric_name, start, end)
    points = raw.get("series", [{}])[0].get("values", [])
    if not points:
        return {"summary": f"No data for {metric_name} in the last {window} hours."}
    # Simple heuristic: compare first vs last point
    first_val = points[0][1]
    last_val = points[-1][1]
    change = last_val - first_val
    change_pct = (change / first_val * 100) if first_val != 0 else float("nan")
    summary = f'From {start:%Y-%m-%d %H:%M} to {end:%Y-%m-%d %H:%M} the metric "{metric_name}" '
    if change_pct > 10:
        summary += f"showed a sharp {change_pct:.1f}% increase. "
    elif change_pct < -10:
        summary += f"showed a sharp {change_pct:.1f}% decrease. "
    else:
        summary += "remained relatively stable. "
    return {"summary": summary}


def __query_metric(metric_name, start, end):
    """Thin wrapper to Datadog query endpoint."""
    import requests

    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": metric_name,
    }
    headers = {
        "DD-API-KEY": API_KEY,
        "DD-APPLICATION-KEY": APP_KEY,
        "Content-Type": "application/json",
    }
    resp = requests.get(BASE_URL + "/query", params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()
