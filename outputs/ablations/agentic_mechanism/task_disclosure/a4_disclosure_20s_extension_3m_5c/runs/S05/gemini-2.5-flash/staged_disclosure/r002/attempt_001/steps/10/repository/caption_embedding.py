import os
import openai

def embed_caption_chunk(caption_chunk: str) -> list[float]:
    """
    Embeds a single caption chunk using OpenAI's embedding model.

    Args:
        caption_chunk: The text chunk to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=[caption_chunk],
        model="text-embedding-ada-002"  # Concrete OpenAI embedding model
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage (for demonstration purposes)
    sample_caption = "The quick brown fox jumps over the lazy dog."
    embedding = embed_caption_chunk(sample_caption)
    print(f"Embedding for '{sample_caption}': {embedding[:5]}...") # Print first 5 elements
