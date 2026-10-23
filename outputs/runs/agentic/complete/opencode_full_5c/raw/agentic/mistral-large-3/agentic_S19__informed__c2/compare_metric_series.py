from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.api import metric_service_v3


class GoogleCloudMonitoringComparator:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"

    def compare_metric_series(
        self,
        metric_type: str,
        filter_a: Dict[str, str],
        filter_b: Dict[str, str],
        hours: int = 1,
        minutes: int = 0,
    ) -> Dict[str, List[Tuple[datetime, float]]]:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours, minutes=minutes)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        def get_series(filter_labels: Dict[str, str]) -> List[Tuple[datetime, float]]:
            metric_filter = f'metric.type="{metric_type}"'
            for key, value in filter_labels.items():
                metric_filter += f' AND metric.labels.{key}="{value}"'

            series_data = []
            for series in self.client.list_time_series(
                name=self.project_name,
                filter=metric_filter,
                interval=interval,
                view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            ):
                for point in series.points:
                    series_data.append(
                        (
                            point.interval.end_time.ToDatetime(),
                            float(point.value.double_value),
                        )
                    )
            return series_data

        return {"series_a": get_series(filter_a), "series_b": get_series(filter_b)}
