from openai import OpenAI
import os
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcript_embedding(transcript_segments: List[str]) -> List[list[float]]:
    response = client.embeddings.create(
        input=transcript_segments, model="text-embedding-3-small"
    )
    return [emb.embedding for emb in response.data]
