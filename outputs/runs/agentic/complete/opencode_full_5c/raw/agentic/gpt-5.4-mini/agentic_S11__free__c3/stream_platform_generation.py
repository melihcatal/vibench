from model_client import get_client
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str, resource: str = None):
    client, target = select_platform_resource(resource)
    return client.responses.stream(
        model=target,
        input=prompt,
    )
