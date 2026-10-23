import os
from embeddings_client import EmbeddingsClient


def embed_text(text: str) -> list[float]:
    client = EmbeddingsClient()
    response = client.embed([text])
    return response.get_embeddings()[0]


if __name__ == "__main__":
    # Example usage
    os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Placeholder for actual key
    text_to_embed = "This is a test sentence."
    embedding = embed_text(text_to_embed)
    # print(f"Embedding for '{text_to_embed}': {embedding[:5]}...") # Print first 5 dimensions
