import os

from openai import OpenAI


def moderation_reason_embedding(text: str, model: str = "text-embedding-3-small"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
