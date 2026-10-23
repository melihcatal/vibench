import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from observability_client import ObservabilityClient
from observability_models import MetricSeries, normalize_metric_response


class MetricsExporter:
    def __init__(self):
        self.b2_key_id = os.getenv("B2_APPLICATION_KEY_ID")
        self.b2_app_key = os.getenv("B2_APPLICATION_KEY")
        self.b2_bucket_name = os.getenv("B2_BUCKET_NAME")

        if not all([self.b2_key_id, self.b2_app_key, self.b2_bucket_name]):
            raise ValueError("Backblaze B2 credentials or bucket name not configured.")

        info = InMemoryAccountInfo()
        self.b2_api = B2Api(info)
        self.b2_api.authorize_account("production", self.b2_key_id, self.b2_app_key)
        self.bucket = self.b2_api.get_bucket_by_name(self.b2_bucket_name)

        self.observability_client = ObservabilityClient()

    def export_metric_snapshot(
        self,
        metric_type: str,
        hours: int = 1,
        filter_labels: Optional[Dict[str, str]] = None,
    ) -> str:
        from google.cloud import monitoring_v3
        from google.api import metric_service_v3

        client = self.observability_client.get_client()
        project_name = self.observability_client.get_project_name()

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        metric_filter = f'metric.type="{metric_type}"'
        if filter_labels:
            filter_parts = self.observability_client.normalize_metric_filter(
                filter_labels
            )
            metric_filter += f" AND {filter_parts}"

        series = client.list_time_series(
            name=project_name,
            filter=metric_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        normalized_series = normalize_metric_response(series)
        snapshot_data = {
            "metric_type": metric_type,
            "time_window": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
            "series": [
                {
                    "resource_labels": s.points[0].resource_labels if s.points else {},
                    "metric_labels": s.points[0].metric_labels if s.points else {},
                    "points": [
                        {"timestamp": p.timestamp.isoformat(), "value": p.value}
                        for p in s.points
                    ],
                }
                for s in normalized_series
            ],
        }

        import json

        snapshot_json = json.dumps(snapshot_data, indent=2)
        snapshot_key = (
            f"metrics/{metric_type}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        )

        self.bucket.upload_bytes(snapshot_json.encode("utf-8"), snapshot_key)

        return f"b2://{self.b2_bucket_name}/{snapshot_key}"
