import google.generativeai as genai
import os


def embed_audit_note(audit_note: str) -> list[float]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # The embedding model to use. You might choose a specific model version here.
    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name, content=audit_note, task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]
