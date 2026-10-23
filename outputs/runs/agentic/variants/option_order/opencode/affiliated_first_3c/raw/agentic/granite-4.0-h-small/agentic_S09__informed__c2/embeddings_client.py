# embeddings_client.py
# [HELPER] Local configuration and client utilities for Direct Embeddings API

import os
from ibm_watsonx_ai import Client


def get_watsonx_client() -> Client:
    """Create and return a WatsonX client instance using environment variables."""
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError(
            "Please set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )
    return Client(api_key=api_key, project_id=project_id)
