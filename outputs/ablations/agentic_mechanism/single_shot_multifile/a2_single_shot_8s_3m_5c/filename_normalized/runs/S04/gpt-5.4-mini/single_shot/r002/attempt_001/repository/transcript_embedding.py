from typing import Any, Dict, List

from openai import OpenAI

from speech_client import get_openai_client


def transcript_embedding(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = get_openai_client()
    texts = [segment.get("text", "") for segment in segments if segment.get("text")]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    data = response.model_dump() if hasattr(response, "model_dump") else response.dict()
    return {"embeddings": data.get("data", []), "model": "text-embedding-3-small", "provider": "openai"}
