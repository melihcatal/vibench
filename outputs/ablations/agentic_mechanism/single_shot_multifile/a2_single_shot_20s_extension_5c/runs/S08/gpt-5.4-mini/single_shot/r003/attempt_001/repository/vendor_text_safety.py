from google import genai
from document_client import load_document_client_config


def moderate_vendor_notes(notes: str) -> dict:
    cfg = load_document_client_config()
    if not cfg.api_key:
        raise ValueError("GOOGLE_API_KEY is required for Google Gemini moderation")
    client = genai.Client(api_key=cfg.api_key)
    response = client.models.generate_content(model="gemini-1.5-flash", contents=f"Moderate this vendor note for unsafe content and return JSON: {notes}")
    text = getattr(response, "text", str(response))
    return {"model": "gemini-1.5-flash", "result": text}
