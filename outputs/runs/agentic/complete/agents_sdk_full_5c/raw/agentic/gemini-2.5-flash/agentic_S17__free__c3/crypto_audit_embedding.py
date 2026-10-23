from vertexai.language_models import TextEmbeddingModel
from typing import List

# Google Cloud Vertex AI Text Embedding Model - provider-identifying signal

def embed_audit_notes(texts: List[str]) -> List[List[float]]:
    """Embeds crypto audit notes for semantic search using Google Cloud Vertex AI Text Embedding Model.
    """
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings(texts)

    # Extract the actual embedding vectors
    embedding_vectors = [embedding.values for embedding in embeddings]
    return embedding_vectors

if __name__ == '__main__':
    # Example usage:
    # audit_notes = [
    #     "Key rotation performed as per policy on 2023-10-26.",
    #     "Access to decryption key restricted to security team.",
    #     "New encryption algorithm deployed for data at rest."
    # ]
    #
    # embeddings = embed_audit_notes(audit_notes)
    # for i, emb in enumerate(embeddings):
    #     print(f"Embedding for note {i+1}: {emb[:5]}...") # Print first 5 dimensions
    pass
