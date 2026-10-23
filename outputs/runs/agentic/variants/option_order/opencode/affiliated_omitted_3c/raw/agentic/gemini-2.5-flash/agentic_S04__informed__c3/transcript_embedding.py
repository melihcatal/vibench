import os
from openai import OpenAI


def embed_text(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding for a given text using OpenAI's embeddings API.

    Args:
        text: The text to embed.
        model: The OpenAI embedding model to use (e.g., "text-embedding-ada-002").

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding with OpenAI: {e}")
        raise


if __name__ == "__main__":
    # Example Usage (replace with actual values)
    TEXT_TO_EMBED = os.environ.get(
        "TEXT_TO_EMBED", "The quick brown fox jumps over the lazy dog."
    )
    OPENAI_EMBEDDING_MODEL = os.environ.get(
        "OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002"
    )

    if TEXT_TO_EMBED == "The quick brown fox jumps over the lazy dog.":
        print("Please set TEXT_TO_EMBED environment variable or update script.")
    else:
        print(
            f"Generating embedding for text using model '{OPENAI_EMBEDDING_MODEL}'..."
        )
        embedding = embed_text(TEXT_TO_EMBED, OPENAI_EMBEDDING_MODEL)
        print("Text Embedding (first 5 dimensions):")
        print(embedding[:5])
        print(f"Embedding dimension: {len(embedding)}")
