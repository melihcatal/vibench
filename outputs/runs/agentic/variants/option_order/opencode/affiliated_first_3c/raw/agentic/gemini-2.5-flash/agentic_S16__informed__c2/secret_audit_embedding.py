import google.generativeai as genai
import os
from typing import List


def embed_audit_notes(notes: List[str]) -> List[List[float]]:
    """Embeds secret audit notes for semantic search using Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # The embedding model to use. Text embedding models are in the text-embedding-xxx family.
    # For details, see https://ai.google.dev/models/gemini
    model = "models/embedding-001"

    embeddings = []
    for note in notes:
        response = genai.embed_content(
            model=model, content=note, task_type="RETRIEVAL_DOCUMENT"
        )
        embeddings.append(response["embedding"])
    return embeddings


if __name__ == "__main__":
    # Example usage
    sample_audit_notes = [
        "User 'admin' accessed 'prod-db-password' for emergency access.",
        "Automated rotation of 'api-key-service-A' completed successfully.",
        "Manual update of 'json-config-dev' due to schema change.",
        "Failed attempt to access 'root-ssh-key' from unknown IP.",
    ]

    # Ensure GOOGLE_API_KEY is set in environment variables
    if "GOOGLE_API_KEY" not in os.environ:
        print("Warning: GOOGLE_API_KEY environment variable not set. Using dummy key.")
        os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    embeddings = embed_audit_notes(sample_audit_notes)
    print("\n--- Audit Note Embeddings ---")
    for i, emb in enumerate(embeddings):
        print(f"Note {i + 1} embedding (first 5 elements): {emb[:5]}...")
