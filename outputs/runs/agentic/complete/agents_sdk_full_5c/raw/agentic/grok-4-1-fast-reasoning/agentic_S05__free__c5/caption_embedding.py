import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_caption_chunks(caption_stream):
    """Embed caption chunks for semantic meeting search using OpenAI Embeddings."""
    for caption in caption_stream:
        if caption.strip():
            response = client.embeddings.create(
                input=caption.strip(),
                model="text-embedding-3-small"
            )
            yield response.data[0].embedding
