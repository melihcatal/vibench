import google.generativeai as genai
import os


def embed_audit_notes(audit_note: str) -> list[float]:
    """
    Embeds crypto audit notes for semantic search using Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Using the embedding-001 model for embeddings
    # https://ai.google.dev/models/gemini#embedding-001
    model = "models/embedding-001"

    response = genai.embed_content(
        model=model,
        content=audit_note,
        task_type="RETRIEVAL_DOCUMENT",  # Specify task type for better performance
    )

    return response["embedding"]


if __name__ == "__main__":
    # Example audit note
    audit_note = "Audit finding: Key rotation policy was not adhered to for key 'prod-data-key' in 'us-east1'."

    try:
        embedding = embed_audit_notes(audit_note)
        print("Crypto Audit Note Embedding (first 5 dimensions):")
        print(embedding[:5])
        print(f"Embedding dimension: {len(embedding)}")
    except Exception as e:
        print(f"Error embedding audit notes: {e}")
