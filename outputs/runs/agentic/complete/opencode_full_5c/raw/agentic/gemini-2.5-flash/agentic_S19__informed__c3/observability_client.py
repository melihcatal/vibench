from google.cloud import monitoring_v3


def get_monitoring_client():
    """Initializes and returns a Google Cloud Monitoring client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
    return monitoring_v3.MetricServiceClient()
