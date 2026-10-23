import os
from openai import OpenAI  # Using OpenAI embeddings API


def embed_caption_chunk(text: str):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",  # Using text-embedding-ada-002 model
            input=[text],
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"OpenAI embedding error: {e}")
        return None
