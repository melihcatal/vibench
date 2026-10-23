from google.cloud import monitoring_v3
from google.api_core.client_options import ClientOptions
import os

def get_monitoring_client():
    """Initializes and returns a Google Cloud Monitoring client."""
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
        
    # For specifying a region, e.g., for regional endpoints
    # client_options = ClientOptions(api_endpoint="monitoring.us-central1-monitoring.googleapis.com")
    # client = monitoring_v3.MetricServiceClient(client_options=client_options)
    
    client = monitoring_v3.MetricServiceClient()
    return client, f"projects/{project_id}"

