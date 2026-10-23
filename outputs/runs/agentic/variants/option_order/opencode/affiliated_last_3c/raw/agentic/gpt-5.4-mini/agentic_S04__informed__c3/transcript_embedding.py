import os

from openai import OpenAI


def transcript_embedding(segments):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    texts = [segment.get("text", "") for segment in segments]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]
