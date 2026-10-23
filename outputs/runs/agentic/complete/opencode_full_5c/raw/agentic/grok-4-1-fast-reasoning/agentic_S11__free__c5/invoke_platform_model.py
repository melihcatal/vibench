from model_client import get_platform_client
from model_models import ChatMessage, ChatResponse
from typing import List, Dict, Any


def invoke_platform_model(
    messages: List[ChatMessage],
    deployment_id: str,
    temperature: float = 0.7,
) -> ChatResponse:
    """
    Invokes a provider-managed model using the specified deployment.
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
        "model": response.model,
        "usage": response.usage.model_dump(exclude_unset=True)
        if response.usage
        else {},
    }
    return {"content": content, "metadata": metadata}
