import json
import requests
from dotenv import load_dotenv

load_dotenv()
from .database_client import DatabaseClient
from .database_models import DatabaseModels

# Google Gemini endpoint (replace with your actual endpoint/key)
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta2/models/chat-bison-001:generateContent"
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")


def translate_text(source_text: str, target_lang: str = "es") -> str:
    """Translate text using Google Gemini chat model (text generation) to produce a translation.
    Provider identifiable: Google Gemini API (requests‑based REST call, GOOGLE_API_KEY env var).
    """
    payload = {
        "temperature": 0.0,
        "messages": [
            {
                "role": "user",
                "content": f"Translate the following text to {target_lang}:",
                "parts": [{"text": source_text}],
            }
        ],
    }
    headers = {
        "Authorization": f"Bearer {GEMINI_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(GEMINI_URL, json=payload, headers=headers)
    resp.raise_for_status()
    response_json = resp.json()
    # The response format for Gemini content generation includes candidate['content']['parts']
    translation = response_json["candidates"][0]["content"]["parts"][0]["text"]
    return translation


def record_translate(
    doc: Dict[str, Any], field: str = "content", target_lang: str = "es"
) -> Dict[str, Any]:
    """Translate the given field of a document using the Gemini API and store the result.
    Returns a normalized document containing the translated text under a new field.
    """
    original = doc.get(field, "")
    translated = translate_text(original, target_lang)
    doc[f"{field}_translated"] = translated
    return DatabaseModels.DocumentResponse(**doc).content
