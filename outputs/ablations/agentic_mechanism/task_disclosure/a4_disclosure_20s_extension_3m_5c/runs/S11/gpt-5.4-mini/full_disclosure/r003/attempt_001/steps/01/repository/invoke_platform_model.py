import os
from typing import Any, Dict, Optional

from anthropic import Anthropic


def invoke_platform_model(
    prompt: str,
    *,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 1024,
    system: Optional[str] = None,
    temperature: Optional[float] = None,
    project_id: Optional[str] = None,
    deployment_id: Optional[str] = None,
    inference_profile_id: Optional[str] = None,
) -> Dict[str, Any]:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    metadata: Dict[str, str] = {}
    if project_id is not None:
        metadata["project_id"] = project_id
    if deployment_id is not None:
        metadata["deployment_id"] = deployment_id
    if inference_profile_id is not None:
        metadata["inference_profile_id"] = inference_profile_id

    params: Dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system is not None:
        params["system"] = system
    if temperature is not None:
        params["temperature"] = temperature
    if metadata:
        params["metadata"] = metadata

    response = client.messages.create(**params)
    content = "".join(block.text for block in response.content if hasattr(block, "text"))
    return {
        "content": content,
        "model": response.model,
        "id": response.id,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }
