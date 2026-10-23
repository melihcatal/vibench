import google.generativeai as genai
from security_client import get_gemini_embedding_model_name


def embed_audit_note(note: str) -> list[float]:
    model_name = get_gemini_embedding_model_name("text-embedding-004")
    response = genai.embed_content(model=model_name, content=note)
    return response["embedding"]
