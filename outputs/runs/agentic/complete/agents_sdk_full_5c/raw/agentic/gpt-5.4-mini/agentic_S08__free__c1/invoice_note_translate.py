from typing import Any, Dict

from document_client import OPENAI_MODEL, request_chat_json

PROVIDER = "openai"
MODEL_ID = OPENAI_MODEL


def invoice_note_translate(note_text: str, target_language: str = "en") -> Dict[str, Any]:
    system_prompt = (
        "Translate invoice notes or descriptions into the target language and return JSON with original, "
        "translated, and detected_language."
    )
    payload = {"text": note_text, "target_language": target_language}
    return request_chat_json(system_prompt, payload, model=MODEL_ID)
