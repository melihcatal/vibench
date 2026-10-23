import os
from openai import OpenAI

def embed_text(text: str) -> list[float]:
    """
    Embeds model outputs for clustering or retrieval using OpenAI's embedding model.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # OpenAI API Key should be set as an environment variable for security
    # e.g., export OPENAI_API_KEY="your_api_key_here"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Using a specific OpenAI embedding model
    # For example, "text-embedding-ada-002" or "text-embedding-3-small"
    model_name = "text-embedding-ada-002"

    try:
        response = client.embeddings.create(
            input=text,
            model=model_name
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error embedding text with OpenAI: {e}")
        return []

if __name__ == "__main__":
    example_text = "This is an example sentence to be embedded."
    embedding = embed_text(example_text)
    if embedding:
        print(f"Embedding for '{example_text}': {embedding[:5]}...") # Print first 5 elements
        print(f"Embedding dimension: {len(embedding)}")
    else:
        print("Failed to generate embedding.")
