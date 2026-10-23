import os
from google.cloud import aiplatform

class ManagedModelClient:
    """
    Provides local configuration and client helper utilities for Managed Model Platform Workflow.
    """
    def __init__(self, project_id: str = None, location: str = None):
        """
        Initializes the client with project ID and location.
        """
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        self.location = location or os.getenv("GCP_LOCATION")

        if not self.project_id:
            raise ValueError("GCP project ID must be provided or set in GCP_PROJECT_ID environment variable.")
        if not self.location:
            raise ValueError("GCP location must be provided or set in GCP_LOCATION environment variable.")

        aiplatform.init(project=self.project_id, location=self.location)
        self.client = aiplatform.gapic.PredictionServiceClient()

    def get_client(self):
        """
        Returns the initialized provider-specific client.
        """
        return self.client
