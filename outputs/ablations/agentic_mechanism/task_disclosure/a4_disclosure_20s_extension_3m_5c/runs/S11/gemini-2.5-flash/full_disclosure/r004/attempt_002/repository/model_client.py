import os
from vertexai.preview.language_models import TextGenerationModel

class ModelClient:
    """
    Provides local configuration and client helper utilities for a Managed Model Platform Workflow.
    """
    def __init__(self, project_id: str = None, location: str = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location or os.getenv("GOOGLE_CLOUD_LOCATION")
        
        if not self.project_id or not self.location:
            raise ValueError("Google Cloud project_id and location must be provided or set as environment variables.")

        # Initialize Vertex AI (Google Cloud specific)
        # In a real application, you would initialize the client here
        # For demonstration, we'll just store the project and location
        self._vertex_ai_model = TextGenerationModel.from_pretrained("text-bison")

    def get_generation_model(self):
        """
        Returns a configured text generation model client.
        """
        return self._vertex_ai_model

    def get_project_id(self) -> str:
        """
        Returns the configured Google Cloud Project ID.
        """
        return self.project_id

    def get_location(self) -> str:
        """
        Returns the configured Google Cloud Location.
        """
        return self.location
