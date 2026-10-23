from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.api import metric_service_v3


class GoogleCloudMonitoringFilter:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"

    def filter_metric_dimensions(
        self,
        metric_type: str,
        dimension_filters: Dict[str, str],
        hours: int = 1,
        minutes: int = 0,
    ) -> List[Dict[str, Tuple[datetime, float]]]:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours, minutes=minutes)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        metric_filter = f'metric.type="{metric_type}"'
        for key, value in dimension_filters.items():
            metric_filter += f' AND metric.labels.{key}="{value}"'

        results = []
        for series in self.client.list_time_series(
            name=self.project_name,
            filter=metric_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        ):
            series_data = {}
            for point in series.points:
                series_data[point.interval.end_time.ToDatetime()] = float(
                    point.value.double_value
                )

            resource_labels = {}
            for label in series.resource.labels:
                resource_labels[label] = series.resource.labels[label]

            results.append({"resource": resource_labels, "data": series_data})

        return results
