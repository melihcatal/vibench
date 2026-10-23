"""
invoice_summary.py

Summarize extracted invoice fields using the Google Gemini API.
"""

import os
import google.generativeai as genai
from typing import Dict, Any, Optional

def summarize_invoice_fields(extracted_invoice_data: Dict[str, Any]) -> Optional[str]:
    """
    Generates a summary of extracted invoice fields using the Google Gemini API.

    Args:
        extracted_invoice_data: A dictionary containing extracted invoice fields.
                                  Expected keys: 'vendor_name', 'transaction_date', 'total_amount', 'currency', 'notes', 'line_items'.

    Returns:
        A string summary of the invoice, or None if the API call fails.
    """
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier

        vendor = extracted_invoice_data.get('vendor_name', 'N/A')
        date = extracted_invoice_data.get('transaction_date', 'N/A')
        total = extracted_invoice_data.get('total_amount', 'N/A')
        currency = extracted_invoice_data.get('currency', 'N/A')
        notes = extracted_invoice_data.get('notes', 'No additional notes.')
        line_items = extracted_invoice_data.get('line_items', [])

        line_item_summary = ""
        if line_items:
            line_item_summary = "Line items:\n"
            for item in line_items:
                desc = item.description if hasattr(item, 'description') and item.description else ''
                amount = item.amount if hasattr(item, 'amount') and item.amount else 'N/A'
                line_item_summary += f"- {desc}: {amount}\n"

        prompt = f"""
        Please summarize the following invoice details concisely:
        Vendor: {vendor}
        Date: {date}
        Total Amount: {total} {currency}
        Notes: {notes}
        {line_item_summary}

        Focus on the most important information for an expense report.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error summarizing invoice: {e}")
        return None
