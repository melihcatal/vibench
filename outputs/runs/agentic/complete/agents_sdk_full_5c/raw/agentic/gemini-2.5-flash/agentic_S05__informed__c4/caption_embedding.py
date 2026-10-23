import os
from openai import OpenAI

# OpenAI Embeddings configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-ada-002"

def embed_caption_chunk(caption_chunk: str) -> list[float]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        input=[caption_chunk],
        model=EMBEDDING_MODEL
    )
    
    # The embedding is usually a list of floats
    return response.data[0].embedding
