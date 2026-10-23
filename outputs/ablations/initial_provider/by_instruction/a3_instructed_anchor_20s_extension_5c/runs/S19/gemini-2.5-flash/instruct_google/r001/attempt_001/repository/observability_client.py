from google.cloud import monitoring_v3

def get_metrics_client():
    return monitoring_v3.MetricServiceClient()
