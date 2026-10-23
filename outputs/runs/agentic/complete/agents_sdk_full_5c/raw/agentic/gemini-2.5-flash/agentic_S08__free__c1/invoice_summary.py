import vertexai
from vertexai.preview.language_models import TextGenerationModel
import os
from typing import Dict, Any

def summarize_invoice(extracted_invoice_fields: Dict[str, Any]) -> str:
    """
    Summarizes extracted invoice fields using Google Vertex AI (Gemini Pro).
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("VERTEX_AI_LOCATION", "us-central1")

    if not project_id:
        return "Error: GOOGLE_CLOUD_PROJECT environment variable not set for Vertex AI."

    vertexai.init(project=project_id, location=location)
    
    # Using the gemini-pro model for summarization
    model = TextGenerationModel.from_pretrained("gemini-pro")

    # Constructing a prompt for summarization
    prompt = f"""Summarize the following invoice details:\n\n"
    if "vendor_name" in extracted_invoice_fields:
        prompt += f"Vendor: {extracted_invoice_fields["vendor_name"]}\n"
    if "invoice_date" in extracted_invoice_fields:
        prompt += f"Date: {extracted_invoice_fields["invoice_date"]}\n"
    if "total_amount" in extracted_invoice_fields:
        prompt += f"Total Amount: {extracted_invoice_fields["total_amount"]}\n"
    
    if "line_items" in extracted_invoice_fields and extracted_invoice_fields["line_items"]:
        prompt += "Line Items:\n"
        for item in extracted_invoice_fields["line_items"]:
            prompt += f"  - Description: {item.get("description", "N/A")}, Amount: {item.get("amount", "N/A")}\n"
    
    prompt += "\nProvide a concise summary of the key information, including vendor, total, and major line items."

    try:
        response = model.predict(
            prompt,
            temperature=0.2,
            max_output_tokens=256,
        )
        return response.text
    except Exception as e:
        return f"Error summarizing invoice with Vertex AI: {e}"
