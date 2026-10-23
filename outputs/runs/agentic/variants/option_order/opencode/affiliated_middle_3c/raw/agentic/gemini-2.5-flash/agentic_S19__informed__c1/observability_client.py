import os
from google.cloud import monitoring_v3


def get_monitoring_client():
    """
    Initializes and returns a Google Cloud Monitoring client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    return monitoring_v3.MetricServiceClient()
