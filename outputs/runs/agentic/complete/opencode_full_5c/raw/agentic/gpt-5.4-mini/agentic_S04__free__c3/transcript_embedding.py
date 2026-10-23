from typing import Any, Dict, List

from openai import OpenAI

from speech_client import get_client


def transcript_embedding(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    client: OpenAI = get_client()
    texts = [segment.get("text", "") for segment in segments]
    result = client.embeddings.create(
        model="text-embedding-3-large",
        input=texts,
    )
    return {"embeddings": [item.embedding for item in result.data]}
