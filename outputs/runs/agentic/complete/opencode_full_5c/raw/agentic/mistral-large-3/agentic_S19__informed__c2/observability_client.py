import os
from typing import Dict, Optional, Any
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
                "Google Cloud credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS or "
                "ensure default credentials are available."
            )

    def get_client(self) -> monitoring_v3.MetricServiceClient:
        return self.client

    def get_project_name(self) -> str:
        return self.project_name

    def validate_metric_type(self, metric_type: str) -> bool:
        try:
            self.client.get_metric_descriptor(
                name=f"{self.project_name}/metricDescriptors/{metric_type}"
            )
            return True
        except Exception:
            return False

    def normalize_metric_filter(
        self, filter_labels: Optional[Dict[str, str]] = None
    ) -> str:
        if not filter_labels:
            return ""
        filter_parts = []
        for key, value in filter_labels.items():
            filter_parts.append(f'metric.labels.{key}="{value}"')
        return " AND ".join(filter_parts)
