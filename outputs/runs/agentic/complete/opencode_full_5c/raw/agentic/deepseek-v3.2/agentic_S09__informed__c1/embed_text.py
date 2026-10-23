import os
from openai import OpenAI


def embed_text(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Generate an embedding vector for one text string using OpenAI Embeddings."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model=model, input=text, encoding_format="float"
    )

    return response.data[0].embedding
