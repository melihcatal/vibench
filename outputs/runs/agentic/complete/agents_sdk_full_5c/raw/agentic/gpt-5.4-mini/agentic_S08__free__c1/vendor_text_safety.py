from typing import Any, Dict

from document_client import OPENAI_MODEL, request_chat_json

PROVIDER = "openai"
MODEL_ID = OPENAI_MODEL


def vendor_text_safety(vendor_notes: str) -> Dict[str, Any]:
    system_prompt = "Moderate vendor notes for policy and safety concerns. Return JSON with label, reasons, and confidence."
    payload = {"text": vendor_notes}
    return request_chat_json(system_prompt, payload, model=MODEL_ID)
