import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from google.cloud import monitoring_v3


def _parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _point_value(point: Any) -> Optional[float]:
    if point.value.int64_value is not None:
        return float(point.value.int64_value)
    if point.value.double_value is not None:
        return float(point.value.double_value)
    if point.value.distribution_value is not None:
        return float(point.value.distribution_value.mean)
    return None


def fetch_series(project_id: str, metric_type: str, window_minutes: int, filter_expr: str) -> List[Dict[str, Any]]:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)
    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )
    series = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}" and {filter_expr}',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    rows = []
    for ts in series:
        for point in ts.points:
            rows.append(
                {
                    "metric": ts.metric.type,
                    "resource_type": ts.resource.type,
                    "resource_labels": dict(ts.resource.labels),
                    "timestamp": point.interval.end_time.ToDatetime().astimezone(timezone.utc).isoformat(),
                    "value": _point_value(point),
                }
            )
    rows.sort(key=lambda item: item["timestamp"])
    return rows


def compare_metric_series(
    project_id: str,
    metric_type: str,
    left_filter: str,
    right_filter: str,
    window_minutes: int = 60,
) -> Dict[str, Any]:
    left = fetch_series(project_id, metric_type, window_minutes, left_filter)
    right = fetch_series(project_id, metric_type, window_minutes, right_filter)
    left_values = [p["value"] for p in left if p["value"] is not None]
    right_values = [p["value"] for p in right if p["value"] is not None]
    return {
        "provider": "google_cloud_monitoring",
        "project_id": project_id,
        "metric_type": metric_type,
        "window_minutes": window_minutes,
        "left": {"filter": left_filter, "points": left, "average": (sum(left_values) / len(left_values)) if left_values else None},
        "right": {"filter": right_filter, "points": right, "average": (sum(right_values) / len(right_values)) if right_values else None},
    }


def main() -> None:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    metric_type = os.environ["METRIC_TYPE"]
    left_filter = os.environ["LEFT_FILTER"]
    right_filter = os.environ["RIGHT_FILTER"]
    window_minutes = int(os.getenv("WINDOW_MINUTES", "60"))
    result = compare_metric_series(project_id, metric_type, left_filter, right_filter, window_minutes)
    print(result)


if __name__ == "__main__":
    main()
