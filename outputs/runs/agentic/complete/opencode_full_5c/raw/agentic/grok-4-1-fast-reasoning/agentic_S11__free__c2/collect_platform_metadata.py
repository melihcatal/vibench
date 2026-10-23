from openai import AzureOpenAI
from model_client import get_azure_openai_config
from model_models import ModelRequest
from typing import Dict, Any


def collect_platform_metadata(request: ModelRequest) -> Dict[str, Any]:
    config = get_azure_openai_config()
    client = AzureOpenAI(**config)
    response = client.chat.completions.create(
        model=request.deployment,
        messages=[msg.model_dump() for msg in request.messages],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return {
        "output": response.choices[0].message.content,
        "metadata": {
            "request_id": response.id,
            "deployment": request.deployment,
            "model": response.model,
            "usage": response.usage.model_dump() if response.usage else None,
            "system_fingerprint": getattr(response, "system_fingerprint", None),
        },
    }
