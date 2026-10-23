import os
import google.generativeai as genai


def embed_audit_notes(text: str) -> list[float]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"  # Using a concrete model identifier
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]


if __name__ == "__main__":
    audit_note = "Audit note: Secret 'db-credentials' accessed by user 'admin' for maintenance on 2023-10-26."
    embedding = embed_audit_notes(audit_note)
    print(f"Embedding for audit note (first 5 elements): {embedding[:5]}...")
    print(f"Embedding dimension: {len(embedding)}")
