import os
from typing import Dict, Any
import google.generativeai as genai
from normalize_expense import NormalizedExpense

def summarize_invoice_fields(normalized_invoice: Dict[str, Any]) -> str:
    # Configure the Google Gemini API
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable must be set.")
    genai.configure(api_key=gemini_api_key)

    # Use the Gemini Pro model for summarization
    model = genai.GenerativeModel('gemini-pro') # Using a concrete model ID

    # Craft a prompt for summarization
    prompt = f"""Summarize the following invoice details in a concise paragraph, highlighting key information like vendor, total amount, and main line items. If no line items, mention just the total and vendor.

Invoice Details:
Vendor: {normalized_invoice.get('vendor_merchant_name', 'N/A')}
Date: {normalized_invoice.get('transaction_date', 'N/A')}
Total Amount: {normalized_invoice.get('total_amount', 'N/A')} {normalized_invoice.get('currency', '')}
Line Items: {', '.join([item.get('description', 'N/A') for item in normalized_invoice.get('items', [])]) if normalized_invoice.get('items') else 'No specific line items.'}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing invoice: {e}"
