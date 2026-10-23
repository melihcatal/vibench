import os
import cohere
from security_models import AuditEmbedding


def embed_secret_audit_note(note: str) -> AuditEmbedding:
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    try:
        response = co.embed(
            texts=[note], model="embed-english-light-v2.0", truncate="RIGHT"
        )
        embedding = response.embeddings[0]
    except cohere.CohereError as e:
        print(f"Error embedding text with Cohere: {e}")
        raise

    return AuditEmbedding(audit_text=note, embedding=embedding)


if __name__ == "__main__":
    audit_note_to_embed = os.environ.get(
        "AUDIT_NOTE", "User admin@example.com accessed secret my/db/password."
    )
    try:
        result = embed_secret_audit_note(audit_note_to_embed)
        print(f"Successfully created embedding for audit note.")
        print(f"  Note: {result.audit_text}")
        print(f"  Embedding vector dimension: {len(result.embedding)}")
    except ValueError as e:
        print(e)
