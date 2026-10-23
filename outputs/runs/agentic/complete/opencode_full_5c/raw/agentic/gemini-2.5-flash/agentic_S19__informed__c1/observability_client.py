from google.cloud import monitoring_v3


def get_monitoring_client():
    """Initializes and returns a Google Cloud Monitoring client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return monitoring_v3.MetricServiceClient()
