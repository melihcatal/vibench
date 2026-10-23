import os
from google.cloud import monitoring_v3


def get_monitoring_client():
    """
    Initializes and returns a Google Cloud Monitoring client.
    Authentication is handled automatically via GOOGLE_APPLICATION_CREDENTIALS
    environment variable.
    """
    # This environment variable should be set to the path of your service account key file.
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        # In a real application, you might raise an exception here.
        # For this example, we'll proceed and let the library handle auth.

    return monitoring_v3.MetricServiceClient()
