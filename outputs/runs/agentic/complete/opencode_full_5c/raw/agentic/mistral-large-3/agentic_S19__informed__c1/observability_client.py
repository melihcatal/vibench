import os
from typing import Dict, List, Optional, Union
from datetime import datetime

from google.cloud import monitoring_v3
from google.api import metric_service_v3
import google.auth
from google.auth.exceptions import DefaultCredentialsError


class ObservabilityClient:
    def __init__(self):
        try:
            self.credentials, self.project_id = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            self.client = monitoring_v3.MetricServiceClient(
                credentials=self.credentials
            )
            self.project_name = f"projects/{self.project_id}"
        except DefaultCredentialsError:
            raise ValueError(
                "Google Cloud credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS "
                "or run in a GCP environment."
            )

    def get_metric_descriptor(
        self, metric_type: str
    ) -> metric_service_v3.MetricDescriptor:
        return self.client.get_metric_descriptor(
            name=f"{self.project_name}/metricDescriptors/{metric_type}"
        )

    def list_metric_descriptors(
        self, filter_str: Optional[str] = None
    ) -> List[metric_service_v3.MetricDescriptor]:
        return list(
            self.client.list_metric_descriptors(
                name=self.project_name, filter=filter_str
            )
        )

    def normalize_metric_data(self, time_series_data: List[Dict]) -> List[Dict]:
        normalized = []
        for data in time_series_data:
            normalized.append(
                {
                    "timestamp": data.get("timestamp"),
                    "value": data.get("value"),
                    "resource": data.get("resource_labels", {}),
                    "metric": data.get("metric_labels", {}),
                }
            )
        return normalized

    def validate_metric_type(self, metric_type: str) -> bool:
        try:
            self.get_metric_descriptor(metric_type)
            return True
        except Exception:
            return False
