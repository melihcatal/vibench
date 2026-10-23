import os
from openai import OpenAI

def embed_caption_chunks(caption_chunks: list[str]) -> list[list[float]]:
    """
    Embeds caption chunks using OpenAI's embedding model for semantic meeting search.

    Args:
        caption_chunks: A list of strings, where each string is a caption chunk.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a caption chunk.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)
    model_name = "text-embedding-ada-002"

    embeddings = []
    for chunk in caption_chunks:
        response = client.embeddings.create(
            input=[chunk],
            model=model_name
        )
        embeddings.append(response.data[0].embedding)

    return embeddings
