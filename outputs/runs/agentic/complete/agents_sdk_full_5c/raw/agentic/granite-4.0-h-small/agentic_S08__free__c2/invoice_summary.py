# [LATER-STEP] invoice_summary.py
"""
Summarize extracted invoice fields using OpenAI completion API.
"""
import json
import openai
from document_models import InvoiceExtractionResponse, NormalizedExpense

def summarize_invoice(extracted: InvoiceExtractionResponse) -> str:
    """Generate a concise textual summary of an invoice.

    Args:
        extracted: Structured fields from upstream extractor.

    Returns:
        Human-readable summary string.
    """
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are an expense report summarizer. Produce a brief, readable summary."},
            {"role": "user", "content": json.dumps(extracted)}
        ]
    }
    response = openai.ChatCompletion.create(**payload)
    # The completion should contain only the summary (placeholder handling)
    return response.choices[0].message.content.strip()
