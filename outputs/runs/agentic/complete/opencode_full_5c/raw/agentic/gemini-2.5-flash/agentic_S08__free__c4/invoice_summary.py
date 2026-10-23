import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from document_models import ExtractedInvoiceFields


class InvoiceSummarizer:
    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        location = os.getenv(
            "GOOGLE_CLOUD_LOCATION", "us-central1"
        )  # Vertex AI often prefers specific regions

        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT_ID environment variable not set for Vertex AI."
            )

        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-pro")  # Using gemini-pro for summarization

    def summarize_invoice(self, invoice_fields: ExtractedInvoiceFields) -> str:
        summary_prompt = f"""
        Summarize the following invoice details concisely:
        Vendor: {invoice_fields.vendor_name or "N/A"}
        Date: {invoice_fields.invoice_date or "N/A"}
        Total Amount: {invoice_fields.total_amount or "N/A"} {invoice_fields.currency or ""}
        Line Items:
        {chr(10).join([f"  - {item.description or ''} (Qty: {item.quantity or 'N/A'}, Unit Price: {item.unit_price or 'N/A'}, Total: {item.total_price or 'N/A'})" for item in invoice_fields.line_items]) or "N/A"}
        
        Provide a brief summary focusing on the key information. Exclude any placeholder text like 'N/A'.
        """

        response = self.model.generate_content(summary_prompt)
        return response.text
