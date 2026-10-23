from typing import List, Dict

from model_client import build_azure_openai_client, load_platform_config
from model_models import PromptRequest, extract_message_text
from select_platform_resource import select_platform_resource


def invoke_platform_model(messages: List[Dict[str, str]]) -> str:
    config = load_platform_config()
    deployment = select_platform_resource(config.deployment)
    client = build_azure_openai_client(config)
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        temperature=0.2,
        max_tokens=256,
    )
    return extract_message_text(response)


def invoke_from_request(request: PromptRequest) -> str:
    return invoke_platform_model(request.messages)
