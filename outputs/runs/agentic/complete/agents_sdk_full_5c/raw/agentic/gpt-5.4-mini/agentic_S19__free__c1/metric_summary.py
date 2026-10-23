from __future__ import annotations

from typing import Any, Dict

from query_metric_window import query_metric_window


def metric_summary(metric_type: str, minutes: int) -> Dict[str, Any]:
    data = query_metric_window(metric_type=metric_type, minutes=minutes)
    values = data.get("values", [])
    trend = "flat"
    if len(values) >= 2:
        trend = "up" if values[-1] > values[0] else "down" if values[-1] < values[0] else "flat"
    anomalies = [v for v in values if v < 0]
    return {"metric_type": metric_type, "trend": trend, "anomalies": anomalies, "sample_count": len(values)}
