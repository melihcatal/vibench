import os
import cohere
from security_models import AuditEmbedding


def embed_audit_notes(audit_text: str) -> AuditEmbedding:
    """
    Embeds secret audit notes for semantic search using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[audit_text], model="embed-english-v3.0", input_type="search_document"
        )
        embedding = response.embeddings[0]
        return AuditEmbedding(audit_note=audit_text, embedding=embedding)
    except Exception as e:
        print(f"Failed to generate embedding: {e}")
        return None


if __name__ == "__main__":
    audit_note = (
        "User 'admin' accessed the secret 'prod/api/key' from IP 192.168.1.100."
    )

    embedding_result = embed_audit_notes(audit_note)

    if embedding_result:
        print(f"Successfully generated embedding for audit note.")
        # print(f"Note: {embedding_result.audit_note}")
        # print(f"Embedding vector (first 5 dimensions): {embedding_result.embedding[:5]}")
        # print(f"Embedding dimension: {len(embedding_result.embedding)}")
    else:
        print("Failed to generate embedding.")
