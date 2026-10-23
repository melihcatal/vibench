
import os
from google.cloud import monitoring_v3

def get_monitoring_client():
    """
    Returns a Google Cloud Monitoring client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return monitoring_v3.MetricServiceClient()

def get_project_id():
    """
    Retrieves the Google Cloud Project ID from the environment variable.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id

def create_metric_descriptor(
    project_id: str,
    metric_type: str,
    metric_kind: monitoring_v3.MetricDescriptor.MetricKind,
    value_type: monitoring_v3.MetricDescriptor.ValueType,
    unit: str,
    description: str,
    display_name: str,
):
    """
    Creates a custom metric descriptor.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"
    descriptor = monitoring_v3.MetricDescriptor()
    descriptor.type = metric_type
    descriptor.metric_kind = metric_kind
    descriptor.value_type = value_type
    descriptor.unit = unit
    descriptor.description = description
    descriptor.display_name = display_name

    try:
        descriptor = client.create_metric_descriptor(
            name=project_name, metric_descriptor=descriptor
        )
        print(f"Created metric descriptor: {descriptor.name}")
        return descriptor
    except Exception as e:
        print(f"Error creating metric descriptor: {e}")
        raise

def write_metric_value(
    project_id: str,
    metric_type: str,
    metric_value: float,
    resource_type: str = "global",
    resource_labels: dict = None,
):
    """
    Writes a custom metric value.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = metric_type
    series.resource.type = resource_type
    if resource_labels:
        series.resource.labels.update(resource_labels)

    point = monitoring_v3.Point()
    point.value.double_value = metric_value
    now = time.time()
    point.interval.end_time.seconds = int(now)
    point.interval.end_time.nanos = int((now - point.interval.end_time.seconds) * 10**9)
    series.points.append(point)

    try:
        client.create_time_series(name=project_name, time_series=[series])
        print(f"Wrote metric value for {metric_type}: {metric_value}")
    except Exception as e:
        print(f"Error writing metric value: {e}")
        raise

import time
