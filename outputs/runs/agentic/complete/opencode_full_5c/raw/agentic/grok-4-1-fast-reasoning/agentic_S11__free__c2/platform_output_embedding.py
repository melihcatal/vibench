from openai import OpenAI
from model_client import get_openai_config
from typing import List, Any


def embed_platform_output(text: str) -> List[float]:
    config = get_openai_config()
    client = OpenAI(**config)
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return [float(x) for x in response.data[0].embedding]
