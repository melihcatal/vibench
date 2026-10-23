from google.cloud import monitoring_v3
import os

def get_monitoring_client():
    """Provides a configured Google Cloud Monitoring MetricServiceClient."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or running in a GCP environment with default credentials.
    return monitoring_v3.MetricServiceClient()

def get_gcp_project_id():
    """Retrieves the GCP project ID from environment variables or a placeholder."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id"))

# Example of how to use it (for local testing/understanding, not part of the core helper)
if __name__ == "__main__":
    client = get_monitoring_client()
    project_id = get_gcp_project_id()
    print(f"Google Cloud Monitoring client initialized: {client}")
    print(f"Using GCP Project ID: {project_id}")
