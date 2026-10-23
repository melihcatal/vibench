import os
import time

from google.api import metric_pb2 as ga_metric
from google.api import monitored_resource_pb2 as ga_monitored_resource
from google.cloud import monitoring_v3

class ObservabilityClient:
    def __init__(self, project_id: str = None):
        if project_id is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if project_id is None:
            raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self.project_id = project_id
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{self.project_id}"

    def write_metric(self, metric_type: str, metric_value: float, resource_type: str = "global"):
        series = monitoring_v3.TimeSeries()
        series.metric.type = metric_type
        series.resource.type = resource_type
        # Add a default label for resource if needed, or allow it to be configured
        # series.resource.labels["project_id"] = self.project_id

        point = monitoring_v3.Point()
        point.interval.end_time.seconds = int(time.time())
        point.value.double_value = metric_value
        series.points.append(point)

        try:
            self.client.create_service_time_series(
                name=self.project_name,
                time_series=[series]
            )
            # print(f"Successfully wrote metric {metric_type} with value {metric_value}")
        except Exception as e:
            # print(f"Error writing metric {metric_type}: {e}")
            raise

    # Placeholder for other utility methods, e.g., to create custom metrics
    def create_custom_metric_descriptor(self, metric_type: str, display_name: str, description: str,
                                        value_type: ga_metric.MetricDescriptor.ValueType,
                                        metric_kind: ga_metric.MetricDescriptor.MetricKind):
        descriptor = ga_metric.MetricDescriptor()
        descriptor.type = metric_type
        descriptor.display_name = display_name
        descriptor.description = description
        descriptor.value_type = value_type
        descriptor.metric_kind = metric_kind

        try:
            self.client.create_metric_descriptor(name=self.project_name, metric_descriptor=descriptor)
            # print(f"Successfully created custom metric descriptor: {metric_type}")
        except Exception as e:
            # print(f"Error creating custom metric descriptor {metric_type}: {e}")
            raise

