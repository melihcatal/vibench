import os
import cohere
from security_models import EmbeddingVector


def create_audit_embedding(audit_note: str) -> EmbeddingVector:
    """
    Embeds secret audit notes for semantic search using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[audit_note], model="embed-english-v3.0", input_type="search_document"
        )
        embedding = response.embeddings[0]
        return EmbeddingVector(text=audit_note, vector=embedding)
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return EmbeddingVector(text=audit_note, vector=[])


if __name__ == "__main__":
    audit_log_notes = "User 'admin' accessed the production database credentials. Justification: Emergency hotfix deployment."

    embedding_result = create_audit_embedding(audit_log_notes)

    if embedding_result.vector:
        print(f"Successfully created embedding for audit note.")
        # print(f"Text: {embedding_result.text}")
        # print(f"Vector (first 5 dimensions): {embedding_result.vector[:5]}...")
        print(f"Vector dimension: {len(embedding_result.vector)}")

    else:
        print("Failed to create embedding.")
