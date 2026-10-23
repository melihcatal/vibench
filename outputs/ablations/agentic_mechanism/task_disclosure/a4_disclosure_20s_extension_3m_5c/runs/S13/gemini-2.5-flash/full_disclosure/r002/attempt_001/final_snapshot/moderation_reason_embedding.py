import os
import openai

def embed_moderation_reason(text: str) -> list[float]:
    """
    Embeds moderation rationales for case retrieval using OpenAI's embedding API.

    Args:
        text: The moderation rationale text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

