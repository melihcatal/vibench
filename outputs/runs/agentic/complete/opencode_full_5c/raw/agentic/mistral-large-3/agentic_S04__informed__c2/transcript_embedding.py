import os
from typing import List, Dict, Any
from openai import OpenAI


def transcript_embedding(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)
    embedded_segments = []

    for segment in segments:
        response = client.embeddings.create(
            input=segment["text"], model="text-embedding-ada-002"
        )
        embedded_segments.append({**segment, "embedding": response.data[0].embedding})
    return embedded_segments
