import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


DEFAULT_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_text(text: str, model: str = DEFAULT_MODEL) -> List[float]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text.strip():
        raise ValueError("text must not be empty")
    response = _client().embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)


def main(text: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    embedding = embed_text(text, model=model)
    return {"model": model, "embedding": embedding}
