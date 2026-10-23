import os
import google.generativeai as genai
from typing import Dict, Any


def summarize_invoice_data(invoice_data: Dict[str, Any]) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""Summarize the following invoice data in a single paragraph:
    
    Vendor: {invoice_data.get("vendor")}
    Date: {invoice_data.get("transaction_date")}
    Total: {invoice_data.get("total")}
    
    Line Items:
    """
    for item in invoice_data.get("line_items", []):
        prompt += (
            f"- {item.get('description', 'N/A')}: {item.get('total_amount', 'N/A')}\n"
        )

    response = model.generate_content(prompt)
    return response.text
