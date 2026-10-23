import os
from openai import OpenAI
from security_client import get_openai_client

def embed_audit_note(audit_note: str) -> list[float]:
    """
    Embeds crypto audit notes for semantic search using OpenAI's embedding API.
    """
    client = get_openai_client()

    try:
        # OpenAI's embedding API is used to convert text into vector embeddings.
        response = client.embeddings.create(
            input=audit_note,
            model="text-embedding-3-small"  # Using a concrete model identifier for embeddings
        )
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        return []

if __name__ == '__main__':
    example_audit_note_1 = "Key rotation for master key 'master-key-prod-us-east-1' completed successfully on 2026-09-19."
    embedding_1 = embed_audit_note(example_audit_note_1)
    print(f"Embedding for Note 1 (first 5 elements): {embedding_1[:5]}...")

    example_audit_note_2 = "Anomaly detected: Multiple failed decryption attempts for 'data-key-finance' on 2026-09-20."
    embedding_2 = embed_audit_note(example_audit_note_2)
    print(f"Embedding for Note 2 (first 5 elements): {embedding_2[:5]}...")
