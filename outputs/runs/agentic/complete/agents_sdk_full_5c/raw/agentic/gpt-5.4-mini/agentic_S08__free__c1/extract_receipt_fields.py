import os
from typing import Any, Dict

from document_client import OPENAI_MODEL, request_chat_json

PROVIDER = "openai"
MODEL_ID = OPENAI_MODEL


def extract_receipt_fields(receipt_text: str) -> Dict[str, Any]:
    system_prompt = (
        "Extract structured receipt fields as JSON with keys merchant, tax, total, currency, and items. "
        "Items should include name, quantity, and amount when available."
    )
    payload = {"document_type": "receipt", "text": receipt_text}
    return request_chat_json(system_prompt, payload, model=os.getenv("OPENAI_RECEIPT_MODEL", MODEL_ID))
