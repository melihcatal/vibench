import os
import google.generativeai as genai
from document_client import validate_env
from document_models import InvoiceExtract
from dataclasses import asdict

validate_env("google_genai")


def invoice_summary(invoice_extract: InvoiceExtract) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    data = asdict(invoice_extract)
    prompt = f"""Provide a concise business summary of this invoice.

Vendor: {data["vendor"]["value"]} (conf: {data["vendor"]["confidence"]:.2f})
Date: {data["date"]["value"]}
Total: ${data["total"]["value"]} (conf: {data["total"]["confidence"]:.2f})
Items ({len(data["line_items"])}): {[li["description"][:30] + "..." if len(li["description"]) > 30 else li["description"] for li in data["line_items"]]}
"""
    response = model.generate_content(prompt)
    return response.text
