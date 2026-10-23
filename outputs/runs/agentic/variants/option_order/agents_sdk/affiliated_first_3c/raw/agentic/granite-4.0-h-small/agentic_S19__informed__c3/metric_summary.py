# metric_summary.py
# LATER-STEP: Summarize recent metric trends or anomalies

from datetime import datetime, timedelta
from typing import List, Dict
import math
import os

# Helper: computes simple anomaly detection based on stddev > 2*σ

def _detect_anomalies(values: List[float]) -> List[float]:
    if len(values) < 2:
        return []
    avg = sum(values) / len(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    std = math.sqrt(variance) if variance > 0 else 0
    return [v for v in values if abs(v - avg) > 2 * std]


def summarize_metric_trends(raw_series: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Accepts the 'data' list used in SAME-SCENARIO responses (timestamp + value).
    Returns a summary dict containing recent trend labels (stable/up/down),
    anomaly timestamps, overall growth/decline percent, and min/max values.
    """
    # Convert timestamps to UTC datetime objects for ordering
    series = sorted(raw_series, key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z','+00:00')))
    if not series:
        return {
            "trend": "no_data",
            "summary": {}
        }
    # Extract values in chronological order
    values = [pt['value'] for pt in series]
    timestamps = [datetime.fromisoformat(pt['timestamp'].replace('Z','+00:00')) for pt in series]
    first_ts = timestamps[0]
    last_ts = timestamps[-1]
    first_val = values[0]
    last_val = values[-1]
    pct_change = (last_val - first_val) / first_val * 100 if first_val != 0 else None

    # Simple trend classification
    if pct_change is None:
        trend = "stable"
    elif pct_change > 5:
        trend = "up"
    elif pct_change < -5:
        trend = "down"
    else:
        trend = "stable"

    anomalies = _detect_anomalies(values)
    anomaly_timestamps = [ts.isoformat() for ts, val in zip(timestamps, values) if val in anomalies]

    summary = {
        "first": {
            "timestamp": first_ts.isoformat(),
            "value": first_val
        },
        "last": {
            "timestamp": last_ts.isoformat(),
            "value": last_val
        },
        "pct_change": round(pct_change, 2) if pct_change is not None else None,
        "trend": trend,
        "anomalies": anomaly_timestamps,
        "min": min(values),
        "max": max(values)
    }
    return {
        "raw": raw_series,
        "summary": summary
    }

# ---------------------------------------------------------------------------
# Example usage
if __name__ == "__main__":
    # Leveraging the SAME-SCENARIO helper (query_metric_window) to get recent data
    import query_metric_window
    import observability_models
    from observability_models import MetricQueryRequest

    now = datetime.utcnow().isoformat() + 'Z'
    one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z'
    request: MetricQueryRequest = {
        "resource_id": os.getenv('AZURE_RESOURCE_ID'),
        "metric_name": os.getenv('AZURE_METRIC_NAME'),
        "start_time": one_hour_ago,
        "end_time": now
    }
    # Call SAME-SCENARIO function directly (alternatively, import from module)
    result = query_metric_window.query_metric_window(
        resource_id=request['resource_id'],
        metric_name=request['metric_name'],
        start_time=one_hour_ago,
        end_time=now
    )
    summary = summarize_metric_trends(result['data'])
    print(summary)
