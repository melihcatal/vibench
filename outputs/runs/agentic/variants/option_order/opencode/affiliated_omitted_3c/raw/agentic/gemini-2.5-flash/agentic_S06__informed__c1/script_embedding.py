import os
from openai import OpenAI


def embed_narration_script(
    text: str, model: str = "text-embedding-ada-002"
) -> list[float]:
    """Embeds narration scripts for voice-asset search using OpenAI Embeddings."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(input=text, model=model)
        return response.data[0].embedding
    except Exception as e:
        raise Exception(f"OpenAI Embedding failed: {e}")
