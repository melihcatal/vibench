import os
from openai import OpenAI
from typing import List


def transcript_embedding(segments: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    client = OpenAI(api_key=api_key)
    return [
        client.embeddings.create(input=seg, model="text-embedding-3-small")
        .data[0]
        .embedding
        for seg in segments
    ]
