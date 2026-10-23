from google.cloud import monitoring_v3


def get_metric_service_client():
    return monitoring_v3.MetricServiceClient()
