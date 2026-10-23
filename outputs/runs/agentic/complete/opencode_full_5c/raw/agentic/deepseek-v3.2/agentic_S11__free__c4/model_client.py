import os
import json
from typing import Dict, Any, Optional
from google.cloud import aiplatform
from google.auth import default


class VertexAIClient:
    """Client helper utilities for Google Cloud Vertex AI."""

    def __init__(
        self, project_id: Optional[str] = None, location: Optional[str] = None
    ):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location or os.environ.get(
            "GOOGLE_CLOUD_LOCATION", "us-central1"
        )

        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        self._init_vertex_ai()

    def _init_vertex_ai(self):
        """Initialize Vertex AI with proper credentials."""
        credentials, _ = default()
        aiplatform.init(
            project=self.project_id, location=self.location, credentials=credentials
        )

    def get_endpoint(self, deployment_name: str) -> aiplatform.Endpoint:
        """Get or create an endpoint for a deployment."""
        endpoint_name = f"projects/{self.project_id}/locations/{self.location}/endpoints/{deployment_name}"
        return aiplatform.Endpoint(endpoint_name=endpoint_name)

    def get_model_parameters(self, model_type: str = "text") -> Dict[str, Any]:
        """Get default parameters for different model types."""
        base_params = {
            "temperature": 0.2,
            "maxOutputTokens": 1024,
            "topP": 0.95,
            "topK": 40,
        }

        model_specific = {
            "text": {"maxOutputTokens": 1024},
            "code": {"temperature": 0.1, "maxOutputTokens": 2048},
            "chat": {"temperature": 0.7, "maxOutputTokens": 512},
            "embedding": {},  # No generation parameters for embeddings
        }

        params = base_params.copy()
        params.update(model_specific.get(model_type, {}))
        return params

    def format_prompt(
        self, prompt: str, system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """Format prompt according to Vertex AI requirements."""
        if system_instruction:
            return {
                "messages": [
                    {"author": "system", "content": system_instruction},
                    {"author": "user", "content": prompt},
                ]
            }
        return {"content": prompt}

    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or environment."""
        if config_path and os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)

        config = {
            "project_id": self.project_id,
            "location": self.location,
            "default_model": os.environ.get("VERTEX_AI_DEFAULT_MODEL", "text-bison"),
            "timeout": int(os.environ.get("VERTEX_AI_TIMEOUT", "30")),
            "max_retries": int(os.environ.get("VERTEX_AI_MAX_RETRIES", "3")),
            "enable_logging": os.environ.get("VERTEX_AI_ENABLE_LOGGING", "true").lower()
            == "true",
        }

        return config

    def validate_deployment(self, deployment_name: str) -> bool:
        """Validate that a deployment exists and is accessible."""
        try:
            endpoint = self.get_endpoint(deployment_name)
            # Try to get endpoint info
            _ = endpoint.display_name
            return True
        except Exception:
            return False


def create_client_from_env() -> VertexAIClient:
    """Create a Vertex AI client from environment variables."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    return VertexAIClient(project_id=project_id, location=location)
