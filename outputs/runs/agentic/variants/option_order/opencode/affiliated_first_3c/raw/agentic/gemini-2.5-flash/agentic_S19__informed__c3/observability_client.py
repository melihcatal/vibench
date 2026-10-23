from google.cloud import monitoring_v3


def get_monitoring_client():
    """
    Provides a Google Cloud Monitoring client.
    The client automatically handles authentication using GOOGLE_APPLICATION_CREDENTIALS.
    """
    return monitoring_v3.MetricServiceClient()
