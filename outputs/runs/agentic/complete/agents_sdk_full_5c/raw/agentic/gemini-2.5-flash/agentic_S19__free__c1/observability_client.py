from google.cloud import monitoring_v3
from google.api import metric_pb2, monitored_resource_pb2

def get_metric_service_client():
    """Returns a Google Cloud Monitoring MetricServiceClient."""
    # Provider-identifying signal: google.cloud.monitoring_v3.MetricServiceClient
    return monitoring_v3.MetricServiceClient()
