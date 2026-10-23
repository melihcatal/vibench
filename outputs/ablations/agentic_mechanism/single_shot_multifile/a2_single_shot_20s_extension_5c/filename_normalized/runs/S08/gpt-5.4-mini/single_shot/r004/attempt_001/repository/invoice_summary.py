from typing import Any, Dict
from openai import OpenAI
from document_client import get_openai_client

SUMMARY_MODEL = "gpt-4.1-mini"


def summarize_invoice_fields(invoice_fields: Dict[str, Any]) -> str:
    client = get_openai_client()
    prompt = (
        "Summarize this invoice in 2-4 concise sentences for a business user. "
        "Highlight vendor, date, total, and notable line items.\n\n"
        f"Invoice JSON:\n{invoice_fields}"
    )
    response = client.responses.create(model=SUMMARY_MODEL, input=prompt, temperature=0)
    return response.output_text
