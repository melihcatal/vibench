import google.generativeai as genai
import os
import json


def summarize_invoice(extracted_invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Gemini.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using a suitable model for summarization

    prompt = f"""Summarize the key information from the following invoice data. 
    Include the vendor, date, total amount, and a brief overview of the line items. 
    Keep the summary concise and in natural language.

    Invoice Data: {json.dumps(extracted_invoice_data, indent=2)}

    Summary:
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error summarizing invoice with Gemini: {e}"
