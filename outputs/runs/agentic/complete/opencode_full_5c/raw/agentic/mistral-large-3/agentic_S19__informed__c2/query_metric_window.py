from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.api import metric_service_v3
from google.api import label_descriptor_pb2


class GoogleCloudMonitoringClient:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"

    def query_metric_window(
        self,
        metric_type: str,
        hours: int = 1,
        minutes: int = 0,
        filter_labels: Optional[Dict[str, str]] = None,
    ) -> List[Tuple[datetime, float]]:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours, minutes=minutes)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        metric_filter = f'metric.type="{metric_type}"'
        if filter_labels:
            for key, value in filter_labels.items():
                metric_filter += f' AND metric.labels.{key}="{value}"'

        results = []
        for result in self.client.list_time_series(
            name=self.project_name,
            filter=metric_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        ):
            for point in result.points:
                results.append(
                    (
                        point.interval.end_time.ToDatetime(),
                        float(point.value.double_value),
                    )
                )

        return results
