import os
from typing import Dict, Any
from model_client import ManagedModelClient
from model_models import GenerationRequest

def collect_platform_metadata(
    deployment_name: str, prompt: str
) -> Dict[str, Any]:
    """Invoke a model and return both output text and rich provider metadata.

    Returns:
        A dict containing:
          - 'text': generated response
          - 'usage': provider usage info (tokens, costs, etc.)
          - 'resource_id': model/deployment identifier used
          - 'raw': full raw response object from the provider SDK
    """
    client = ManagedModelClient()
    request = GenerationRequest(
        deployment=deployment_name,
        prompt=prompt,
        temperature=0.5,
        max_tokens=512,
    )
    response = client.invoke_generation(request)
    # response.raw holds the provider-specific raw payload (e.g., OpenAI CompletionResponse)
    return {
        "text": response.text,
        "usage": response.usage,
        "resource_id": response.deployment_id,
        "raw": response.raw,
    }
