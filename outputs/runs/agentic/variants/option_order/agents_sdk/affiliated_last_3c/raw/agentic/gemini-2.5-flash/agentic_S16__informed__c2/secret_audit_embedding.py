import os
import google.generativeai as genai

def embed_audit_note(audit_note: str) -> list[float]:
    """
    Generates an embedding for a secret audit note using Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # The embedding model to use
    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name,
        content=audit_note,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY to be set)
    note1 = "Audit log: Secret 'db_user_prod' updated due to quarterly rotation policy."
    note2 = "Audit log: Access granted to 'dev_team' for 'test_api_key'."
    note3 = "Audit log: Secret 'db_user_dev' updated as part of incident response."

    try:
        embedding1 = embed_audit_note(note1)
        print(f"Embedding for note 1 (first 5 values): {embedding1[:5]}...")

        embedding2 = embed_audit_note(note2)
        print(f"Embedding for note 2 (first 5 values): {embedding2[:5]}...")

        embedding3 = embed_audit_note(note3)
        print(f"Embedding for note 3 (first 5 values): {embedding3[:5]}...")

    except Exception as e:
        print(f"Error generating embedding: {e}")
