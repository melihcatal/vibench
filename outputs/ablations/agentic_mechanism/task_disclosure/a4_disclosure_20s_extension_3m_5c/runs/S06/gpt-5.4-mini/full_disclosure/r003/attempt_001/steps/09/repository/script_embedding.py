import os
from typing import List

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_narration_scripts(scripts: List[str]) -> List[List[float]]:
    client = _client()
    response = client.embeddings.create(model="text-embedding-3-large", input=scripts)
    return [item.embedding for item in response.data]
