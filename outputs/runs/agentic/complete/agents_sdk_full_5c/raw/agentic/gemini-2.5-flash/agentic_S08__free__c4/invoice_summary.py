import os
from typing import Optional
from google.cloud import aiplatform
from google.cloud.aiplatform.generative_models import GenerationConfig, GenerativeModel, Part
from document_models import ExtractedInvoice

def summarize_invoice(
    invoice_data: ExtractedInvoice,
    project_id: str,
    location: str,
    model_name: str = "gemini-pro",
    temperature: float = 0.4,
    max_output_tokens: int = 200,
) -> Optional[str]:
    """Summarizes extracted invoice fields using Google Cloud Vertex AI generative models."""

    try:
        aiplatform.init(project=project_id, location=location)
        model = GenerativeModel(model_name)

        prompt_template = """Summarize the following invoice details concisely:

Vendor Name: {vendor_name}
Invoice Date: {invoice_date}
Total Amount: {total_amount} {currency}
Line Items: {line_items_summary}
Notes: {notes}

Provide a summary that highlights the key information, such as who the invoice is from, the date, the total amount, and a brief overview of the items. Keep it to 2-3 sentences.
"""

        line_items_summary = "; ".join([f"{item.description} ({item.total_amount or 'N/A'} {invoice_data.currency or ''})" for item in invoice_data.line_items])
        if not line_items_summary and invoice_data.line_items:
            line_items_summary = f"{len(invoice_data.line_items)} items"
        elif not line_items_summary:
            line_items_summary = "No specific line items mentioned."

        formatted_prompt = prompt_template.format(
            vendor_name=invoice_data.vendor_name or "N/A",
            invoice_date=invoice_data.invoice_date or "N/A",
            total_amount=invoice_data.total_amount or "N/A",
            currency=invoice_data.currency or "",
            line_items_summary=line_items_summary,
            notes=invoice_data.notes or "None"
        )

        generation_config = GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )

        response = model.generate_content(
            formatted_prompt,
            generation_config=generation_config,
        )

        return response.text.strip()

    except Exception as e:
        print(f"Error summarizing invoice with Vertex AI: {e}")
        return None
