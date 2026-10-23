import os
from openai import OpenAI

def embed_script(script_text: str) -> list[float]:
    """
    Embeds narration scripts for voice-asset search using OpenAI.

    Args:
        script_text: The narration script text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input=script_text,
        model="text-embedding-3-small"
    )
    
    return response.data[0].embedding
