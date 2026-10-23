from typing import List, Dict, Any
from model_client import get_platform_client
from model_models import build_chat_request
from select_platform_resource import select_platform_resource

def invoke_platform_model(
    messages: List[Dict[str, str]],
    model_hint: str = "gpt-4o"
) -> str:
    """
    Invokes a provider-managed model through project-scoped platform client.
    """
    client = get_platform_client()
    deployment = select_platform_resource(model_hint)
    request = build_chat_request(messages)
    response = client.chat.completions.create(
        model=deployment,
        **request
    )
    return response.choices[0].message.content
