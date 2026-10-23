import os
from typing import Dict, Any
from google.cloud import aiplatform

def summarize_invoice(extracted_invoice_data: Dict[str, Any]) -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID must be set in environment variables.")

    aiplatform.init(project=project_id, location=location)

    # Using a text-bison model for summarization
    model = aiplatform.GenerativeModel("gemini-pro") # Using gemini-pro for summarization

    vendor = extracted_invoice_data.get("vendor", "N/A")
    date = extracted_invoice_data.get("date", "N/A")
    total = extracted_invoice_data.get("total", "N/A")
    line_items = extracted_invoice_data.get("line_items", [])

    line_item_summary = ""
    if line_items:
        line_item_summary = "\nLine Items:\n"
        for item in line_items:
            description = item.get("description", "")
            quantity = item.get("quantity", "")
            amount = item.get("amount", "")
            line_item_summary += f"- {description} (Qty: {quantity}, Amt: {amount})\n"

    prompt = f"Summarize the following invoice details:\n\nVendor: {vendor}\nDate: {date}\nTotal: {total}{line_item_summary}\n\nProvide a concise summary of the invoice."

    response = model.generate_content(prompt)
    return response.text
