import os
from google.cloud import monitoring_v3

# ----------- LOCAL HELPER ------------
# GCP Monitoring provider integration utilities

def get_client() -> monitoring_v3.MetricServiceClient:
    """Create and return a GCP Monitoring metric client using environment variables for authentication."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS points to a service account JSON
    return monitoring_v3.MetricServiceClient()

# Optional: helper to translate GCP metric descriptors into our internal model
# expose for later-step files if needed
