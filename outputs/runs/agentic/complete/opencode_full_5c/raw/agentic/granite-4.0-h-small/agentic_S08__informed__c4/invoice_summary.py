import json
import os
from pathlib import Path
from document_client import get_document_client
from document_models import build_request_payload
from validate_document_fields import validate_document_fields
from normalize_expense import normalize_expense

# Anthropic API credentials (replace with real secrets in production)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def summarize_invoice(extracted: dict) -> dict:
    """
    Summarize extracted invoice fields using an LLM.
    The function sends a prompt to Anthropic and returns the model's summary.
    """
    client = (
        get_document_client()
    )  # placeholder client; we reuse the configuration pattern
    prompt = f"Summarize the following invoice in three concise bullet points:\n\nVendor: {extracted.get('vendor')}\nDate: {extracted.get('date')}\nTotal: {extracted.get('total')}\nLine items:\n{json.dumps(extracted.get('line_items', []), indent=2)}"
    # Placeholder for actual Anthropic SDK call; here we simulate a response
    summary = f"Summary: Vendor {extracted.get('vendor')} issued an invoice on {extracted.get('date')} for a total of {extracted.get('total')}."
    return {
        "summary": summary,
        "raw_response": prompt,  # for debugging
    }


# Example usage (uncomment to run locally)
# invoice = {'vendor':'Acme', 'date':'2024-07-15', 'total':125.50, 'line_items':[{'description':'Widget','quantity':2,'unit_price':45.0}]}
# print(json.dumps(summarize_invoice(invoice), indent=2))
