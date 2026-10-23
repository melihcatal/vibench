from openai import AzureOpenAI

from model_client import build_platform_client, load_platform_config
from model_models import normalize_text


def platform_output_embedding(text: str) -> list[float]:
    config = load_platform_config()
    client: AzureOpenAI = build_platform_client(config)
    response = client.embeddings.create(model="text-embedding-3-small", input=normalize_text(text))
    return list(response.data[0].embedding)
