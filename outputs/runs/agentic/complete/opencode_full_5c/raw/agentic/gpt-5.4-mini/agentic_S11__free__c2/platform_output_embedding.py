from openai import OpenAI

from model_client import build_platform_client, load_platform_config
from model_models import normalize_text


def platform_output_embedding(text: str) -> list[float]:
    cfg = load_platform_config()
    client: OpenAI = build_platform_client(cfg)
    result = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_text(text)
    )
    return result.data[0].embedding
