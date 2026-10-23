from openai import OpenAI

from model_client import get_client
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str, resource: str = None):
    client, target = select_platform_resource(resource)
    return client.responses.create(
        model=target,
        input=prompt,
    )
