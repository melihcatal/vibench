from __future__ import annotations

from observability_client import CloudWatchMetricsClient
from observability_models import MetricComparison, MetricSeriesPoint, MetricWindowRequest, normalize_datetime


def compare_metric_series(left: MetricWindowRequest, right: MetricWindowRequest) -> MetricComparison:
    client = CloudWatchMetricsClient()
    left_resp = client.list_metric_data(
        metric_name=left.metric_name,
        start_time=left.start_time,
        end_time=left.end_time,
        dimensions=left.dimensions,
        period=left.period,
        stat=left.statistic,
    )
    right_resp = client.list_metric_data(
        metric_name=right.metric_name,
        start_time=right.start_time,
        end_time=right.end_time,
        dimensions=right.dimensions,
        period=right.period,
        stat=right.statistic,
    )

    def to_points(response, dims):
        pts = []
        for item in response.get("Datapoints", []):
            value = item.get(left.statistic, item.get("Average"))
            if value is not None:
                pts.append(MetricSeriesPoint(timestamp=normalize_datetime(item["Timestamp"]), value=float(value), unit=item.get("Unit"), dimensions=dims))
        return sorted(pts, key=lambda p: p.timestamp)

    return MetricComparison(
        metric_name=left.metric_name,
        left_label=str(left.dimensions or "left"),
        right_label=str(right.dimensions or "right"),
        points_left=to_points(left_resp, left.dimensions),
        points_right=to_points(right_resp, right.dimensions),
    )
