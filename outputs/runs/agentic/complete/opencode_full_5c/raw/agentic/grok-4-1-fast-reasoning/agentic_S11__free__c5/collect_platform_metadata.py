from model_client import get_platform_client
from model_models import ChatMessage, ChatResponse
from typing import List, Dict, Any


def collect_platform_metadata(
    messages: List[ChatMessage],
    deployment_id: str,
    temperature: float = 0.7,
) -> ChatResponse:
    """
    Collects model output with full platform metadata.
    """
    client = get_platform_client()
    response = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
        temperature=temperature,
        stream=False,
    )
    content = response.choices[0].message.content or ""
    metadata = {
        "id": response.id,
        "object": response.object,
        "created": response.created,
        "model": response.model,
        "system_fingerprint": getattr(response, "system_fingerprint", None),
        "usage": response.usage.model_dump(exclude_unset=True)
        if response.usage
        else {},
    }
    return {"content": content, "metadata": metadata}
