from typing import Dict, Optional
import os
from datetime import datetime, timedelta
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
        minutes: int = 0,
        filter_labels: Optional[Dict[str, str]] = None,
    ) -> Dict[str, float]:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours, minutes=minutes)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        metric_filter = f'metric.type="{metric_type}"'
        if filter_labels:
            for key, value in filter_labels.items():
                metric_filter += f' AND metric.labels.{key}="{value}"'

        aggregation = monitoring_v3.Aggregation(
            alignment_period=timedelta(minutes=1),
            per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            group_by_fields=["resource.*"],
        )

        results = self.client.list_time_series(
            name=self.project_name,
            filter=metric_filter,
            interval=interval,
            aggregation=aggregation,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        stats = {"mean": 0.0, "min": float("inf"), "max": float("-inf"), "count": 0}

        for series in results:
            for point in series.points:
                value = float(point.value.double_value)
                stats["mean"] += value
                stats["min"] = min(stats["min"], value)
                stats["max"] = max(stats["max"], value)
                stats["count"] += 1

        if stats["count"] > 0:
            stats["mean"] /= stats["count"]
        else:
            stats["min"] = 0.0
            stats["max"] = 0.0

        return stats
