from typing import Any, Dict, List

from translation_client import create_openai_embedding


def translation_memory_embedding(segments: List[str]) -> Dict[str, Any]:
    payload = create_openai_embedding(segments, model="text-embedding-3-small")
    return {
        "provider": "openai_embeddings",
        "model": "text-embedding-3-small",
        "embeddings": [item.get("embedding", []) for item in payload.get("data", [])],
    }
