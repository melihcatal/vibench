import os
from google.cloud import logging
from google.cloud import logging_v2

def get_logging_client() -> logging.Client:
    """Provides a configured Google Cloud Logging client for log ingestion."""
    # Client will automatically pick up GOOGLE_APPLICATION_CREDENTIALS or default credentials
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    return logging.Client()

def get_logging_query_client(project_id: str) -> logging_v2.Client:
    """Provides a configured Google Cloud Logging v2 client for log querying."""
    # Client will automatically pick up GOOGLE_APPLICATION_CREDENTIALS or default credentials
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    return logging_v2.Client(project=project_id)

if __name__ == "__main__":
    # Example usage:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        try:
            ingestion_client = get_logging_client()
            print(f"Successfully initialized Google Cloud Logging ingestion client for project: {ingestion_client.project}")

            query_client = get_logging_query_client(project_id)
            print(f"Successfully initialized Google Cloud Logging query client for project: {query_client.project}")

        except Exception as e:
            print(f"Error initializing logging clients: {e}")
