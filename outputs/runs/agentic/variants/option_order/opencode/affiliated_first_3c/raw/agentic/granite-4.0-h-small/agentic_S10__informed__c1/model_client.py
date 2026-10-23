import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import ServiceDefinition

# Configuration via environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Singleton client for the inference service (Watsonx Granite)
_client = None


def get_client() -> APIClient:
    """Return a singleton Watsonx API client configured for Granite model inference."""
    global _client
    if _client is None:
        if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
            raise RuntimeError(
                "Environment variables WATSONX_API_KEY and WATSONX_PROJECT_ID must be set"
            )
        _client = APIClient(
            api_key=WATSONX_API_KEY,
            project_id=WATSONX_PROJECT_ID,
            service=ServiceDefinition.WATSONX_AI_TEXT_CHAT,  # Granite inference endpoint
        )
    return _client
