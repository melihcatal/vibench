# [SAME-SCENARIO] invoke_platform_model.py
# IBM watsonx.ai implementation

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import WATSONX_API_KEY, WATSONX_PROJECT_ID


def invoke_model(deployment_id: str, prompt: str, max_tokens: int = 256) -> dict:
    """Invoke a watsonx.ai managed model deployment.

    Args:
        deployment_id: The model deployment ID.
        prompt: Prompt text to send to the model.
        max_tokens: Max tokens for the response.

    Returns:
        Dict containing model output and provider metadata.
    """
    api_key = os.getenv(WATSONX_API_KEY)
    project_id = os.getenv(WATSONX_PROJECT_ID)
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    client = APIClient(api_key=api_key, project_id=project_id)
    # Example using the `llama2` family model - replace with your deployment name
    deployment_name = f"{deployment_id}---text-completion"
    response = client.text_generation.complete(
        deployment_name=deployment_name,
        messages=[{"content": prompt}],
        max_tokens=max_tokens,
    )
    # Gather metadata
    metadata = {
        "provider": "watsonx.ai",
        "deployment_id": deployment_id,
        "request_id": response.get_request_id(),
        "usage": response.get_usage(),  # usage details if available
    }
    # Normalize response to a simple string (you can keep full structure if needed)
    result = {"output": response.get_result(), "metadata": metadata}
    return result
