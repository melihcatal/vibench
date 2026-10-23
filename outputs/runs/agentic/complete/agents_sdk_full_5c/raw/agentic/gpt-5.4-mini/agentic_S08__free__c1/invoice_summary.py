from typing import Any, Dict

from document_client import OPENAI_MODEL, request_chat_json

PROVIDER = "openai"
MODEL_ID = OPENAI_MODEL


def invoice_summary(invoice_fields: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = "Summarize extracted invoice fields into concise business-friendly JSON with summary and risk_flags."
    payload = {"invoice_fields": invoice_fields}
    return request_chat_json(system_prompt, payload, model=MODEL_ID)
