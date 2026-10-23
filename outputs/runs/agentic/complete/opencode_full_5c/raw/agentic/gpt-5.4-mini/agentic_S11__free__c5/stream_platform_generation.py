from model_client import create_platform_client
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str):
    client = create_platform_client()
    model = select_platform_resource()
    return client.responses.stream(model=model, input=prompt)
