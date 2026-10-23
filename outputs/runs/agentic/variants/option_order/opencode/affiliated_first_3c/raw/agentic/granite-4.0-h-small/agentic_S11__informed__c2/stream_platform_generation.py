# [SAME-SCENARIO] stream_platform_generation.py
# Streams a watsonx.ai model response while preserving provider metadata

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.genai import GenerativeModel
from typing import Iterator, Any


def stream_model(prompt: str, deployment_id: str) -> Iterator[dict]:
    """Stream output from a watsonx model and yield each generation object.

    Yields:
        Dictionaries containing the partial text and associated metadata.
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
        stream=True,
    )
    for gen in response.generations:
        yield {
            "partial_text": gen.text,
            "usage": gen.usage,
            "metadata": gen.metadata,
        }
