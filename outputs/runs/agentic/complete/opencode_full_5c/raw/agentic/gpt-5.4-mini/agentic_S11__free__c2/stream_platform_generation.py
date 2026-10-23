from openai import OpenAI

from model_client import build_platform_client, load_platform_config
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str):
    cfg = load_platform_config()
    client: OpenAI = build_platform_client(cfg)
    model_id = select_platform_resource(cfg.model)
    return client.responses.create(model=model_id, input=prompt, stream=True)
