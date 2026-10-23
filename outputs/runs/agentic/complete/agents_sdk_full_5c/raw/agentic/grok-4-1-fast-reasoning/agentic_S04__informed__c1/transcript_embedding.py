import os
from openai import OpenAI

def transcript_embedding(texts):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    if isinstance(texts, str):
        texts = [texts]
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [embedding.embedding for embedding in response.data]