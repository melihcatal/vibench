import os
from embeddings_client import EmbeddingsClient


def embed_batch(texts: list[str]) -> list[list[float]]:
    client = EmbeddingsClient()
    response = client.embed(texts)
    return response.get_embeddings()


if __name__ == "__main__":
    # Example usage
    os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Placeholder for actual key
    texts_to_embed = ["Hello world.", "How are you?", "Batch embedding example."]
    embeddings = embed_batch(texts_to_embed)
    # for i, emb in enumerate(embeddings):
    #     print(f"Embedding for '{texts_to_embed[i]}': {emb[:5]}...") # Print first 5 dimensions
