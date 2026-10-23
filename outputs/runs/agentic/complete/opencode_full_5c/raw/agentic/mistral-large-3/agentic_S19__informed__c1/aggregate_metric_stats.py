import os
from datetime import datetime, timedelta
from typing import Dict, Optional

from google.cloud import monitoring_v3
from google.api import metric_service_v3


class GoogleCloudMonitoringAggregator:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"

    def aggregate_metric_stats(
        self,
        metric_type: str,
        hours: int = 1,
        filter_labels: Optional[Dict[str, str]] = None,
    ) -> Dict:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        metric_filter = f'metric.type="{metric_type}"'
        if filter_labels:
            for key, value in filter_labels.items():
                metric_filter += f' AND metric.labels.{key}="{value}"'

        aggregation = monitoring_v3.Aggregation(
            alignment_period=timedelta(minutes=1),
            per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            group_by_fields=["resource.*", "metric.*"],
        )

        results = self.client.list_time_series(
            name=self.project_name,
            filter=metric_filter,
            interval=interval,
            aggregation=aggregation,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        stats = {
            "count": 0,
            "mean": 0.0,
            "min": float("inf"),
            "max": float("-inf"),
            "sum": 0.0,
            "series": [],
        }

        for series in results:
            for point in series.points:
                value = point.value.double_value
                stats["count"] += 1
                stats["sum"] += value
                stats["min"] = min(stats["min"], value)
                stats["max"] = max(stats["max"], value)
                stats["series"].append(
                    {
                        "resource_labels": dict(series.resource.labels),
                        "metric_labels": dict(series.metric.labels),
                        "value": value,
                    }
                )

        if stats["count"] > 0:
            stats["mean"] = stats["sum"] / stats["count"]

        return stats
