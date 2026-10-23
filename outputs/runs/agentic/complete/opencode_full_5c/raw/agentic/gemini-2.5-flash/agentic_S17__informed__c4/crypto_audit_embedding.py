import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def embed_audit_note(note_text: str) -> list[float]:
    model = "embedding-001"
    response = genai.embed_content(
        model=model, content=note_text, task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]
