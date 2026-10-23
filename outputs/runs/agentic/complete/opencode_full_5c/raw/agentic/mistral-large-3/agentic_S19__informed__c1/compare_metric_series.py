import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

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
    ) -> Dict:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        def build_filter(base_filter: Dict[str, str]) -> str:
            metric_filter = f'metric.type="{metric_type}"'
            for key, value in base_filter.items():
                if key.startswith("resource."):
                    metric_filter += f' AND resource.label.{key[9:]}="{value}"'
                else:
                    metric_filter += f' AND metric.labels.{key}="{value}"'
            return metric_filter

        filter_a_str = build_filter(filter_a)
        filter_b_str = build_filter(filter_b)

        results = {}
        for label, metric_filter in [
            ("series_a", filter_a_str),
            ("series_b", filter_b_str),
        ]:
            series_data = []
            for time_series in self.client.list_time_series(
                name=self.project_name,
                filter=metric_filter,
                interval=interval,
                view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            ):
                for point in time_series.points:
                    series_data.append(
                        {
                            "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                            "value": point.value.double_value,
                            "resource_labels": dict(time_series.resource.labels),
                            "metric_labels": dict(time_series.metric.labels),
                        }
                    )
            results[label] = series_data

        comparison = {
            "series_a": results["series_a"],
            "series_b": results["series_b"],
            "comparison_stats": {
                "series_a_count": len(results["series_a"]),
                "series_b_count": len(results["series_b"]),
                "series_a_avg": sum(d["value"] for d in results["series_a"])
                / len(results["series_a"])
                if results["series_a"]
                else 0,
                "series_b_avg": sum(d["value"] for d in results["series_b"])
                / len(results["series_b"])
                if results["series_b"]
                else 0,
                "difference": (
                    sum(d["value"] for d in results["series_a"])
                    - sum(d["value"] for d in results["series_b"])
                )
                if results["series_a"] and results["series_b"]
                else None,
            },
        }
        return comparison
