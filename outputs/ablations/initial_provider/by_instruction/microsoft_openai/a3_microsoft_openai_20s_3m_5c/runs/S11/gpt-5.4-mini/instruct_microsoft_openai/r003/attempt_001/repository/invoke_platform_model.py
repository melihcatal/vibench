from openai import AzureOpenAI

from model_client import build_platform_client, load_platform_config
from model_models import PlatformPrompt, extract_message_text
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str) -> str:
    config = load_platform_config()
    client: AzureOpenAI = build_platform_client(config)
    deployment = select_platform_resource(config.deployment)
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": PlatformPrompt(prompt).text}],
    )
    return extract_message_text(response)
