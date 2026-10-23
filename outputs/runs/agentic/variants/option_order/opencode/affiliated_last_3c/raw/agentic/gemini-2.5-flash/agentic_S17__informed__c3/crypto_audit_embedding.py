import google.generativeai as genai
import os


def embed_audit_note(audit_note: str) -> list[float]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(
        "embedding-001"
    )  # Use an embedding model like embedding-001

    # The embedding model creates a vector representation of the text.
    response = model.embed_content(model=model.model_name, content=audit_note)

    # The embedding is a list of floats.
    return response["embedding"]
