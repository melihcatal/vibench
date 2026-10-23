from google import genai
from document_client import load_document_client_config


def translate_invoice_note(note: str, target_language: str = "en") -> str:
    cfg = load_document_client_config()
    if not cfg.api_key:
        raise ValueError("GOOGLE_API_KEY is required for Google Gemini translation")
    client = genai.Client(api_key=cfg.api_key)
    response = client.models.generate_content(model="gemini-1.5-pro", contents=f"Translate this invoice note to {target_language}: {note}")
    return getattr(response, "text", str(response))
