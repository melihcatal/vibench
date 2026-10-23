from typing import List
from embeddings_client import get_embeddings_client


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of text strings.
    """
    client = get_embeddings_client()
    embeddings = client.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]


if __name__ == "__main__":
    texts_to_embed = ["Hello, world!", "This is a test.", "Embedding a batch of texts."]
    batch_embeddings = generate_embeddings_batch(texts_to_embed)
    for i, embedding in enumerate(batch_embeddings):
        print(f"Embedding for text {i + 1}: {embedding[:5]}...")
