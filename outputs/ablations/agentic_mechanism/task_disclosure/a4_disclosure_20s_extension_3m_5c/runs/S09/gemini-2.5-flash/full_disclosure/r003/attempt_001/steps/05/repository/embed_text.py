import os
import openai

def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using OpenAI's API.

    Args:
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    text_to_embed = "Hello, world!"
    embedding = embed_text(text_to_embed)
    print(f"Embedding for '{text_to_embed}': {embedding[:5]}...") # Print first 5 elements
    print(f"Embedding length: {len(embedding)}")
