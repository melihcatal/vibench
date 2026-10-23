import os
from google.cloud import monitoring_v3

def get_monitoring_client():
    # Credentials are typically picked up automatically from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS) or GKE service account.
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    return monitoring_v3.MetricServiceClient()
