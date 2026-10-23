import os
from typing import List
from openai import OpenAI

def transcript_embedding(segments: List[str]) -> List[List[float]]:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable is required.')
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(input=segments, model='text-embedding-3-small')
    return [emb.embedding for emb in response.data]