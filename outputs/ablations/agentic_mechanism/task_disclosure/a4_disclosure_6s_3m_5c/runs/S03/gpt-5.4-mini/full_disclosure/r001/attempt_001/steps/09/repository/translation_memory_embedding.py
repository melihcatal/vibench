import os
from typing import List, Dict, Any, Optional

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_translated_segments(segments: List[str], model: Optional[str] = None) -> List[Dict[str, Any]]:
    client = _client()
    embedding_model = model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    response = client.embeddings.create(model=embedding_model, input=segments)
    return [
        {"text": segment, "embedding": item.embedding, "index": index}
        for index, (segment, item) in enumerate(zip(segments, response.data))
    ]
