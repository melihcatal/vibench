import openai
import os

def embed_transcript_segments(segments: list[str]) -> list[list[float]]:
    """
    Embeds transcript segments for semantic retrieval using OpenAI's embedding API.

    Args:
        segments: A list of text segments to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    # Ensure the OpenAI API key is set as an environment variable
    # For example: export OPENAI_API_KEY='your_api_key_here'
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()
    model = "text-embedding-ada-002"  # Concrete OpenAI embedding model

    response = client.embeddings.create(
        input=segments,
        model=model
    )

    embeddings = [data.embedding for data in response.data]
    return embeddings
