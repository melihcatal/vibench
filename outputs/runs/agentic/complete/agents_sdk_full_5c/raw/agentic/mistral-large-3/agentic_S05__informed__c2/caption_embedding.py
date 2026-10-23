import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
_openai_client = OpenAI(api_key=OPENAI_API_KEY)


def embed_caption(caption: str) -> list[float]:
    if not caption.strip():
        return []
    response = _openai_client.embeddings.create(
        input=caption,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding