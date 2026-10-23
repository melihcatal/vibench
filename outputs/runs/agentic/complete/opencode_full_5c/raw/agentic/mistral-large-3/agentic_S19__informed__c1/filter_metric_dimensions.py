import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from google.cloud import monitoring_v3
from google.api import metric_service_v3


class GoogleCloudMonitoringFilter:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"

    def filter_metric_dimensions(
        self, metric_type: str, dimension_filters: Dict[str, str], hours: int = 1
    ) -> List[Dict]:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        metric_filter = f'metric.type="{metric_type}"'
        for key, value in dimension_filters.items():
            if key.startswith("resource."):
                metric_filter += f' AND resource.label.{key[9:]}="{value}"'
            else:
                metric_filter += f' AND metric.labels.{key}="{value}"'

        results = []
        for time_series in self.client.list_time_series(
            name=self.project_name,
            filter=metric_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        ):
            for point in time_series.points:
                results.append(
                    {
                        "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                        "value": point.value.double_value,
                        "resource_labels": dict(time_series.resource.labels),
                        "metric_labels": dict(time_series.metric.labels),
                    }
                )
        return results
