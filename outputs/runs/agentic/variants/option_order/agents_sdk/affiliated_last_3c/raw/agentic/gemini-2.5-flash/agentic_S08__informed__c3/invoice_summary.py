import google.generativeai as genai
import os
from document_client import get_gemini_config

def summarize_invoice_fields(invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Gemini API.
    """
    config = get_gemini_config()
    genai.configure(api_key=config["api_key"])

    model = genai.GenerativeModel(config["model_name"])

    prompt = f"""
    Please summarize the following invoice data in a concise manner, highlighting key information like vendor, total amount, and a brief overview of line items.

    Invoice Data: {invoice_data}
    """

    response = model.generate_content(prompt)
    return response.text
