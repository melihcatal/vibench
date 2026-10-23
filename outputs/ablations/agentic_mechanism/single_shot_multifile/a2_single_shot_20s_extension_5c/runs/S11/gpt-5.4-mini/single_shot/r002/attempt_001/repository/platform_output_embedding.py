from typing import Any, Dict, List

from openai import OpenAI

from model_client import get_openai_client

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_platform_output(text: str, client: OpenAI | None = None) -> Dict[str, Any]:
    api_client = client or get_openai_client()
    response = api_client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    vector: List[float] = response.data[0].embedding if getattr(response, "data", None) else []
    return {"provider": "openai", "model": EMBEDDING_MODEL, "embedding": vector, "raw": response}
