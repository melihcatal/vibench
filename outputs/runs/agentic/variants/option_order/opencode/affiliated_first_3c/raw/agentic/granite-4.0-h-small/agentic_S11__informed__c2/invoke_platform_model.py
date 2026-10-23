# [SAME-SCENARIO] invoke_platform_model.py
# Uses IBM watsonx.ai as the managed model platform

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.genai import GenerativeModel


def invoke_model(prompt: str, deployment_id: str) -> dict:
    """Invoke a watsonx.ai generative model and return its response.

    Args:
        prompt: The input text prompt.
        deployment_id: The watsonx deployment identifier for the model.

    Returns:
        A dict containing the model's generated text and metadata.
    """
    # Load credentials from environment
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise ValueError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    client = APIClient(api_key=api_key, project_id=project_id)
    model = GenerativeModel(
        foundation_model="ibm/granite-13b-v2",
        project_id=project_id,
        api_key=api_key,
    )

    response = model.generate_messages(
        deployment_id=deployment_id,
        messages=[{"role": "user", "content": prompt}],
    )

    # The response includes usage and model metadata
    return {
        "generated_text": response.generations[0].text,
        "usage": response.usage,
        "model_handle": model.handle,
        "metadata": response.metadata,
    }
