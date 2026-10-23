import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os

def summarize_invoice_fields(invoice_fields: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud's Generative AI.

    Args:
        invoice_fields: A dictionary containing extracted invoice fields
                        (e.g., vendor_name, date, total_amount, items, etc.).

    Returns:
        A string containing the summary of the invoice fields.
    """
    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION"))
    model = GenerativeModel("gemini-pro")

    prompt_parts = [
        "Please summarize the following invoice fields:
",
        f"Vendor Name: {invoice_fields.get("vendor_name", "N/A")}
",
        f"Date: {invoice_fields.get("date", "N/A")}
",
        f"Total Amount: {invoice_fields.get("total_amount", "N/A")}
",
        "Items:
"
    ]

    items = invoice_fields.get("items", [])
    if items:
        for item in items:
            prompt_parts.append(f"- Description: {item.get("description", "N/A")}, Quantity: {item.get("quantity", "N/A")}, Unit Price: {item.get("unit_price", "N/A")}, Amount: {item.get("amount", "N/A")}
")
    else:
        prompt_parts.append("- No items found.
")

    response = model.generate_content("".join(prompt_parts))
    return response.text
