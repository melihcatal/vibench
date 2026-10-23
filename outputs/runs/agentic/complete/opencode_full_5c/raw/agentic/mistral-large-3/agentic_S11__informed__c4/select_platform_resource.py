from typing import Dict, Any, Optional
import os
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai import APIClient


def select_platform_resource(
    model_id: str = "mistralai/mistral-large-latest",
) -> Dict[str, Any]:
    """
    Resolves a watsonx.ai model resource for invocation.
    Requires WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        raise ValueError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be set.")

    client = APIClient(
        credentials={"apikey": api_key, "url": "https://us-south.ml.cloud.ibm.com"}
    )

    model = Model(model_id=model_id, params={"project_id": project_id}, client=client)

    return {
        "model": model,
        "model_id": model_id,
        "provider": "watsonx.ai",
        "client": client,
    }
