import openai
import os

def embed_script(script_text: str) -> list[float]:
    """
    Embeds narration scripts for voice-asset search using OpenAI's embedding service.

    Args:
        script_text: The narration script as a string.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=script_text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

