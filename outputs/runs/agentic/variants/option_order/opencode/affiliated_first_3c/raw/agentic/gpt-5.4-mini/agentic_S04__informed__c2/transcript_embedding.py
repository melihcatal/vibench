from typing import Any, Dict, List

from openai import OpenAI


def transcript_embedding(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI()
    texts = [segment.get("text", "") for segment in segments]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return {
        "model": "text-embedding-3-small",
        "embeddings": [item.embedding for item in response.data],
    }
