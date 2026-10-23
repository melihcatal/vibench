from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_sections(sections: List[str], model: str = DEFAULT_EMBEDDING_MODEL) -> Dict[str, Any]:
    client = OpenAI(api_key=__import__("os").getenv("OPENAI_API_KEY"))
    if not __import__("os").getenv("OPENAI_API_KEY"):
        raise ValueError("Missing required environment variable: OPENAI_API_KEY")
    response = client.embeddings.create(model=model, input=sections)
    embeddings = [item.embedding for item in response.data]
    return {
        "provider": "openai",
        "model": model,
        "embeddings": embeddings,
        "usage": getattr(response, "usage", None),
    }
