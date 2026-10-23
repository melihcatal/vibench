from ibm_watsonx_ai import Credentials
from typing import Dict, Any
import os


def get_watsonx_config() -> Credentials:
    """Load WatsonX.ai credentials from environment variables."""
    return Credentials(
        url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
        api_key=os.getenv("WATSONX_API_KEY"),
        project_id=os.getenv("WATSONX_PROJECT_ID")
    )


def get_client_config() -> Dict[str, Any]:
    """Return a generic client configuration for reuse."""
    return {
        "api_key": os.getenv("WATSONX_API_KEY"),
        "project_id": os.getenv("WATSONX_PROJECT_ID"),
        "url": os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    }