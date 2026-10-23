import os
import google.generativeai as genai

def embed_audit_note(audit_note: str) -> list[float]:
    # Configure the Gemini API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use the embedding model
    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name,
        content=audit_note,
        task_type="RETRIEVAL_DOCUMENT"
    )

    # The embedding is a list of floats
    return response['embedding']
