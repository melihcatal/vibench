import os
from typing import Optional, Dict, Any
from google.cloud import monitoring_v3
from google.auth import default
from google.auth.transport.requests import Request
import google.api_core.exceptions


class ObservabilityClient:
    """Client helper utilities for Google Cloud Monitoring."""

    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the observability client.

        Args:
            project_id: Google Cloud project ID. If None, will try to get from environment or default credentials.
        """
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            try:
                _, self.project_id = default()
            except Exception:
                raise ValueError(
                    "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
                )

        self.monitoring_client = None
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize Google Cloud Monitoring client."""
        try:
            self.monitoring_client = monitoring_v3.MetricServiceClient()
        except Exception as e:
            print(f"Failed to initialize Monitoring client: {e}")
            raise

    def get_project_name(self) -> str:
        """Get the full project name for API calls."""
        return f"projects/{self.project_id}"

    def test_connection(self) -> bool:
        """Test connection to Google Cloud Monitoring."""
        try:
            project_name = self.get_project_name()
            list_request = monitoring_v3.ListMetricDescriptorsRequest(
                name=project_name, page_size=1
            )
            self.monitoring_client.list_metric_descriptors(request=list_request)
            return True
        except google.api_core.exceptions.GoogleAPICallError as e:
            print(f"Connection test failed: {e}")
            return False
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def get_available_metrics(
        self, filter_prefix: Optional[str] = None, page_size: int = 100
    ) -> list:
        """
        Get available metrics in the project.

        Args:
            filter_prefix: Optional prefix to filter metrics (e.g., 'compute.googleapis.com/')
            page_size: Number of metrics to return per page

        Returns:
            List of metric descriptors
        """
        try:
            project_name = self.get_project_name()

            filter_str = None
            if filter_prefix:
                filter_str = f'metric.type = starts_with("{filter_prefix}")'

            list_request = monitoring_v3.ListMetricDescriptorsRequest(
                name=project_name, filter=filter_str, page_size=page_size
            )

            metrics = []
            for metric in self.monitoring_client.list_metric_descriptors(
                request=list_request
            ):
                metrics.append(
                    {
                        "type": metric.type,
                        "name": metric.display_name,
                        "description": metric.description,
                        "metric_kind": metric.metric_kind.name,
                        "value_type": metric.value_type.name,
                        "unit": metric.unit,
                        "labels": [
                            {"key": label.key, "description": label.description}
                            for label in metric.labels
                        ],
                    }
                )

            return metrics

        except google.api_core.exceptions.GoogleAPICallError as e:
            print(f"Error getting available metrics: {e}")
            raise

    def get_metric_descriptor(self, metric_type: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed descriptor for a specific metric.

        Args:
            metric_type: Full metric type name

        Returns:
            Metric descriptor dictionary or None if not found
        """
        try:
            project_name = self.get_project_name()
            metric_name = f"{project_name}/metricDescriptors/{metric_type}"

            descriptor = self.monitoring_client.get_metric_descriptor(name=metric_name)

            return {
                "type": descriptor.type,
                "name": descriptor.display_name,
                "description": descriptor.description,
                "metric_kind": descriptor.metric_kind.name,
                "value_type": descriptor.value_type.name,
                "unit": descriptor.unit,
                "labels": [
                    {"key": label.key, "description": label.description}
                    for label in descriptor.labels
                ],
            }

        except google.api_core.exceptions.NotFound:
            print(f"Metric descriptor not found: {metric_type}")
            return None
        except google.api_core.exceptions.GoogleAPICallError as e:
            print(f"Error getting metric descriptor: {e}")
            raise

    def get_default_time_range(self, hours: int = 1) -> tuple:
        """
        Get default time range for queries.

        Args:
            hours: Number of hours to look back

        Returns:
            Tuple of (start_time, end_time) as datetime objects
        """
        from datetime import datetime, timedelta

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        return start_time, end_time

    def build_filter_string(
        self, metric_type: str, filters: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build filter string for metric queries.

        Args:
            metric_type: Metric type name
            filters: Optional resource or metric label filters

        Returns:
            Filter string
        """
        filter_parts = [f'metric.type = "{metric_type}"']

        if filters:
            for key, value in filters.items():
                if key.startswith("metric."):
                    label_key = key.replace("metric.", "")
                    filter_parts.append(f'metric.labels.{label_key} = "{value}"')
                else:
                    filter_parts.append(f'resource.labels.{key} = "{value}"')

        return " AND ".join(filter_parts)

    @staticmethod
    def get_environment_info() -> Dict[str, Any]:
        """
        Get environment information for debugging.

        Returns:
            Dictionary with environment info
        """
        env_vars = {}
        for key in [
            "GOOGLE_CLOUD_PROJECT",
            "GOOGLE_APPLICATION_CREDENTIALS",
            "GOOGLE_CLOUD_QUOTA_PROJECT",
        ]:
            if key in os.environ:
                env_vars[key] = os.environ[key]

        return {
            "environment_variables": env_vars,
            "python_version": os.sys.version,
            "working_directory": os.getcwd(),
        }
