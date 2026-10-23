from typing import List

from openai import OpenAI

from model_client import build_client, load_config


def embed_platform_output(text: str) -> List[float]:
    config = load_config()
    client: OpenAI = build_client(config)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding
