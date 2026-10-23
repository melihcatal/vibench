import os
from openai import OpenAI

def embed_text(text: str) -> list[float]:
    """
    Embeds model outputs for clustering or retrieval using OpenAI embeddings.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )

    return response.data[0].embedding
