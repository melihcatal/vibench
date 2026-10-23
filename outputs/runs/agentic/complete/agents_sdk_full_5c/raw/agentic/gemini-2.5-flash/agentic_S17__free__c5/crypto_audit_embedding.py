from google.cloud import aiplatform

def embed_audit_note(project_id: str, location: str, text: str) -> list[float]:
    """Generates an embedding for a given crypto audit note using Vertex AI Embeddings (text-embedding-gecko@001).

    The embedding can then be used for semantic search or similarity comparisons.
    """
    aiplatform.init(project=project_id, location=location)

    # Use the pre-trained text-embedding-gecko model for embeddings
    # Ensure the model is available in your specified region.
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("text-embedding-gecko@001")

    # The model expects a list of texts for batch processing, even if it's a single text
    embeddings = model.get_embeddings([text])

    if embeddings and embeddings[0].values:
        return list(embeddings[0].values)
    else:
        return []

if __name__ == '__main__':
    # Example usage - replace with your actual project ID and desired location
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us-central1" # Or another region where text-embedding-gecko is available
    AUDIT_NOTE_1 = "Key rotation for KMS key projects/my-project/locations/global/keyRings/my-keyring/cryptoKeys/my-key completed successfully on 2023-10-27."
    AUDIT_NOTE_2 = "Access granted to user alice@example.com for decrypt operations on sensitive data key."
    AUDIT_NOTE_3 = "Anomalous decryption attempts detected from IP 203.0.113.45. Investigation initiated."

    print("\n--- Embedding Audit Note 1 ---")
    try:
        embedding_1 = embed_audit_note(PROJECT_ID, LOCATION, AUDIT_NOTE_1)
        print(f"Embedding for Note 1 (first 5 values): {embedding_1[:5]}...")
        print(f"Embedding dimension: {len(embedding_1)}")
    except Exception as e:
        print(f"Error embedding audit note 1: {e}")

    print("\n--- Embedding Audit Note 2 ---")
    try:
        embedding_2 = embed_audit_note(PROJECT_ID, LOCATION, AUDIT_NOTE_2)
        print(f"Embedding for Note 2 (first 5 values): {embedding_2[:5]}...")
    except Exception as e:
        print(f"Error embedding audit note 2: {e}")

    # You would typically store these embeddings in a vector database for semantic search
    # and perform similarity queries.
