"""Local configuration and client helper utilities for Managed Metrics Monitoring.

Provides a shared Google Cloud Monitoring client setup and credential
resolution for the observability integration layer.
"""

import os
from typing import Optional

from google.cloud.monitoring_v3 import MetricServiceClient


class ObservabilityConfig:
    """Holds configuration for Google Cloud Monitoring connections."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        self.project_id = project_id or os.environ.get("GCP_PROJECT_ID")
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

    def ensure_project(self) -> str:
        if not self.project_id:
            raise ValueError(
                "GCP_PROJECT_ID environment variable is required for "
                "Google Cloud Monitoring queries."
            )
        return self.project_id

    def ensure_credentials(self) -> str:
        if not self.credentials_path or not os.path.isfile(self.credentials_path):
            raise FileNotFoundError(
                "GOOGLE_APPLICATION_CREDENTIALS must point to a valid "
                "service account JSON file for Google Cloud Monitoring."
            )
        return self.credentials_path


def create_metric_service_client(
    config: Optional[ObservabilityConfig] = None,
) -> MetricServiceClient:
    """Create a google.cloud.monitoring_v3.MetricServiceClient.

    The client authenticates using GOOGLE_APPLICATION_CREDENTIALS as managed
    by the Google Cloud SDK environment.
    """
    cfg = config or ObservabilityConfig()
    cfg.ensure_credentials()
    return MetricServiceClient()


def build_monitored_resource_name(
    project_id: str,
) -> str:
    """Build the Google Cloud project parent resource string."""
    return f"projects/{project_id}"


def build_metric_type(metric_name: str) -> str:
    """Convert a shorthand metric name to a full Google Cloud metric type.

    Examples:
        'compute.googleapis.com/instance/cpu/utilization' -> unchanged
        'cpu/utilization' -> 'compute.googleapis.com/instance/cpu/utilization'
    """
    if "/" in metric_name and "." in metric_name:
        return metric_name
    domain_map = {
        "cpu": "compute.googleapis.com/instance/cpu",
        "memory": "compute.googleapis.com/instance/memory",
        "disk": "compute.googleapis.com/instance/disk",
        "network": "compute.googleapis.com/instance/network",
    }
    parts = metric_name.split("/", 1)
    prefix = domain_map.get(parts[0], "compute.googleapis.com/instance")
    return f"{prefix}/{parts[-1]}" if len(parts) > 1 else f"{prefix}/{parts[0]}"
