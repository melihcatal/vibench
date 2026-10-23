import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_caption_chunks(caption: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=caption
    )
    return response.data[0].embedding
