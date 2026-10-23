import os
import openai
from openai import OpenAI


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def embed_text(text, model="text-embedding-3-small"):
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding
