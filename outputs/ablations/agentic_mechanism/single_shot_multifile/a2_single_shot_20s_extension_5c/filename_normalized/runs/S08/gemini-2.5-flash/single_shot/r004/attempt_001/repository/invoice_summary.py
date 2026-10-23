import json
import google.generativeai as genai
from document_client import get_google_genai_model
from document_models import NormalizedExpense
from typing import Dict, Any

def summarize_invoice_gemini(invoice_data: NormalizedExpense) -> str:
    """
    Summarizes key fields from a normalized invoice using Google Generative AI (Gemini Pro).
    Requires GOOGLE_API_KEY environment variable.
    """
    model = get_google_genai_model("gemini-pro")

    invoice_dict = invoice_data.model_dump(exclude_unset=True)

    prompt = f"""
    Summarize the key information from the following expense document.
    Focus on the primary vendor, transaction date, total amount, and a brief overview of line items if present.
    If the document type is an invoice, mention that.
    Provide the summary in a concise paragraph.

    Expense Document Data:
    {json.dumps(invoice_dict, indent=2)}
    """

    response = model.generate_content(prompt)
    return response.text
