import os
from typing import Any, Dict

from document_client import get_extraction_client

SUMMARY_MODEL_ID = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")


def invoice_summary(invoice_fields: Dict[str, Any]) -> Dict[str, Any]:
    client = get_extraction_client()
    prompt = {
        "task": "summarize_invoice",
        "model": SUMMARY_MODEL_ID,
        "invoice_fields": invoice_fields,
    }
    return client.extract_with_openai(model=SUMMARY_MODEL_ID, request=type("R", (), {"document_type": "invoice_summary", "to_prompt": lambda self, schema_name: __import__("json").dumps(prompt)})(), schema_name="invoice_summary")
