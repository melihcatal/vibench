import openai
import os

def embed_caption_chunks(caption_chunks: list[str]) -> list[list[float]]:
    """
    Embeds caption chunks using OpenAI's embedding API.

    Args:
        caption_chunks: A list of string caption chunks.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    embeddings = []
    for chunk in caption_chunks:
        response = openai.embeddings.create(
            input=[chunk],
            model="text-embedding-ada-002"
        )
        embeddings.append(response.data[0].embedding)
    return embeddings
