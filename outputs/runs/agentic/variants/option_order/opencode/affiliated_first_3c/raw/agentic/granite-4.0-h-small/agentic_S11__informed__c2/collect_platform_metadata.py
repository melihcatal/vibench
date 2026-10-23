# [SAME-SCENARIO] collect_platform_metadata.py
# Returns model output together with watsonx platform metadata

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.genai import GenerativeModel
from typing import Dict


def collect_metadata(prompt: str, deployment_id: str) -> dict:
    """Invoke a watsonx model and bundle the generated text with platform metadata.

    Returns:
        A dict containing 'generated_text', 'usage', 'resource_id', 'metadata', etc.
    """
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

    return {
        "generated_text": response.generations[0].text,
        "usage": response.usage,
        "resource_id": model.handle,
        "metadata": response.metadata,
    }
