from typing import List

from openai import OpenAI

from model_client import get_openai_client


def platform_output_embedding(text: str) -> List[float]:
    client: OpenAI = get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return list(response.data[0].embedding)
