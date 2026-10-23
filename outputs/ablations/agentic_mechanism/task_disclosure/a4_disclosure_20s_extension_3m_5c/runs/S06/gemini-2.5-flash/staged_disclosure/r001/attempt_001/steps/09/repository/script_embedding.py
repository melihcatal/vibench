import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_script(script: str) -> list[float]:
    """Embeds a narration script using Google's text-embedding-004 model."""
    vertexai.init() # Initializes the Vertex AI SDK
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([script])
    return embeddings[0].values

if __name__ == "__main__":
    # Example usage (can be removed if not needed for final submission)
    sample_script = "This is a sample narration script for testing purposes."
    embedding = embed_script(sample_script)
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 embedding values: {embedding[:5]}")
