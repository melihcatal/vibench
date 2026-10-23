from typing import List, Dict, Any

from .model_client import get_azure_openai_client


def invoke_platform_model(
    messages: List[Dict[str, str]], deployment: str, **kwargs: Any
) -> Any:
    client = get_azure_openai_client(deployment)
    response = client.chat.completions.create(messages=messages, **kwargs)
    return response
