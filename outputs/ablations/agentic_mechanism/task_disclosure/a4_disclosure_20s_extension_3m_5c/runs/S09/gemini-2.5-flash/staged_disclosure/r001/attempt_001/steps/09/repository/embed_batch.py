import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embeddings for a batch of texts using Google's Vertex AI.

    Args:
        texts: A list of texts to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    vertexai.init()
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]

if __name__ == "__main__":
    example_texts = [
        "Hello world",
        "How are you?",
        "This is a test sentence.",
    ]
    batch_embeddings = embed_batch(example_texts)
    for i, embedding in enumerate(batch_embeddings):
        print(f"Embedding for '{example_texts[i]}': {embedding[:5]}...") # Print first 5 dimensions
