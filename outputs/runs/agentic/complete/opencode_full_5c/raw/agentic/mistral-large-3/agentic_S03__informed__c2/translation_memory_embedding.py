from typing import List
from openai import OpenAI
import os
import numpy as np


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "text-embedding-ada-002"

    embeddings = []
    for segment in segments:
        response = client.embeddings.create(input=segment, model=model)
        embeddings.append(response.data[0].embedding)

    return embeddings
