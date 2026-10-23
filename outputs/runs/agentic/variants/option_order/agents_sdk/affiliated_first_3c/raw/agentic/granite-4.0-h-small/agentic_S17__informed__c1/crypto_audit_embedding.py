import os
from google.cloud import kms
from google.cloud.aiplatform import embeddings
from security_client import get_kms_client

def crypto_audit_embedding(key_name: str, audit_note: str) -> None:
    """Creates an embedding for a crypto audit note and writes it to an LLM embedding store.
    Uses Google Cloud KMS to encrypt the audit note before sending it to the embedding service.
    Assumes the embedding service uses Google Cloud AI Platform embeddings endpoint.
    """
    # 1. Encrypt audit note with KMS
    kms_client = get_kms_client()
    response = kms_client.encrypt(
        name=key_name,
        plaintext=audit_note.encode("utf-8")
    )
    encrypted_note = response.ciphertext
    # 2. Create a plain-text representation for the model (model will embed the decrypted version later)
    # For demo we send the encrypted bytes as a base64 string to the embedding API
    import base64
    note_for_embedding = f"ENCRYPTED_NOTE:{base64.b64encode(encrypted_note).decode()}"
    # 3. Call embeddings endpoint (using Watsonx.ai SDK as example)
    client = embeddings.EmbeddingsClient()
    embedding = client.embed_content(
        content=note_for_embedding,
        content_type=embeddings.DataType.TEXT
    )
    # embedding.id, embedding.embedding.vector available
    print("Embedding ID:", embedding.id)
    print("Embedding vector length:", len(embedding.embedding.vector))

if __name__ == "__main__":
    # Example usage (requires WATSONX_API_KEY and WATSONX_PROJECT_ID env vars)
    project_id = os.getenv("GCLOUD_PROJECT")
    location_id = "global"
    key_ring_id = "my-key-ring"
    crypto_key_id = "my-audit-key"
    key_path = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    note = "User accessed key 'my-key' at 2025-08-15 12:34 UTC. Purpose: data protection."
    crypto_audit_embedding(key_path, note)
