from typing import Dict, List, Any

from model_client import build_azure_openai_client, load_platform_config
from model_models import extract_message_text
from select_platform_resource import select_platform_resource


def collect_platform_metadata(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    config = load_platform_config()
    deployment = select_platform_resource(config.deployment)
    client = build_azure_openai_client(config)
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        temperature=0.2,
        max_tokens=256,
    )
    return {
        "text": extract_message_text(response),
        "model": getattr(response, "model", deployment),
        "usage": getattr(response, "usage", None),
        "response_id": getattr(response, "id", None),
        "resource_id": deployment,
    }
