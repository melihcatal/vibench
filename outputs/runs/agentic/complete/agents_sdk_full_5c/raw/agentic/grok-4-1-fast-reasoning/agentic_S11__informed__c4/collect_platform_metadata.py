from typing import Dict, Any, List
from model_client import get_platform_client
from model_models import build_chat_request, extract_content, extract_usage
from select_platform_resource import select_platform_resource

def collect_platform_metadata(
    messages: List[Dict[str, str]],
    model_hint: str = "gpt-4o"
) -> Dict[str, Any]:
    """
    Returns model output together with provider platform metadata.
    """
    client = get_platform_client()
    deployment = select_platform_resource(model_hint)
    request = build_chat_request(messages)
    response = client.chat.completions.create(
        model=deployment,
        **request
    )
    return {
        "output": extract_content(response),
        "usage": extract_usage(response),
        "model": response.model,  # deployment ID
        "id": response.id,
        "created": response.created,
        "system_fingerprint": getattr(response, "system_fingerprint", None),
    }
