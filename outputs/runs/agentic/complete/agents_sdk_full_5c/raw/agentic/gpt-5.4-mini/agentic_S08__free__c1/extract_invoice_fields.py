import os
from typing import Any, Dict

from document_client import OPENAI_MODEL, request_chat_json

PROVIDER = "openai"
MODEL_ID = OPENAI_MODEL


def extract_invoice_fields(invoice_text: str) -> Dict[str, Any]:
    system_prompt = (
        "Extract structured invoice fields as JSON with keys vendor, date, total, currency, "
        "and line_items. Each line item should include description, quantity, unit_price, and amount."
    )
    payload = {"document_type": "invoice", "text": invoice_text}
    return request_chat_json(system_prompt, payload, model=os.getenv("OPENAI_INVOICE_MODEL", MODEL_ID))
