import os
from typing import Dict, List

# Example using Google Document AI for invoice extraction
from google.cloud import documentai_v1 as documentai

# Load creds from env variable set by Google Cloud SDK

class InvoiceExtractor:
    def __init__(self, project_id: str, processor_id: str, location: str = "us"):
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_full_id = self.client.processor_path(project_id, location, processor_id)

    def extract(self, invoice_bytes: bytes) -> Dict:
        # Prepare the document payload
        document = {"content": invoice_bytes, "mime_type": "application/pdf"}
        # Send request
        response = self.client.process_document(
            name=self.processor_full_id, document=document
        )
        # Parse entities – this example assumes the processor returns fields named 'vendor', 'date', 'total', 'line_items'
        entities = response.document.entities
        result = {}
        for ent in entities:
            if ent.type_ == "vendor":
                result["vendor"] = ent.mention_text
            elif ent.type_ == "date":
                result["date"] = ent.mention_text
            elif ent.type_ == "total":
                result["total"] = float(ent.mention_text.replace(",", ""))
            elif ent.type_ == "line_item":
                # collect all line items
                if "line_items" not in result:
                    result["line_items"] = []
                result["line_items"].append({"description": ent.mention_text})
        return result

# Helper function for the scored pipeline
def extract_invoice_fields(invoice_path: str) -> Dict:
    # Read invoice as bytes (PDF, JPG, PNG are supported)
    with open(invoice_path, "rb") as f:
        invoice_bytes = f.read()
    # Instantiate extractor – credentials are read from env vars (GOOGLE_APPLICATION_CREDENTIALS)
    extractor = InvoiceExtractor(
        project_id=os.getenv("GOOGLE_PROJECT_ID"),
        processor_id=os.getenv("GOOGLE_INVOICE_PROCESSOR_ID"),
    )
    return extractor.extract(invoice_bytes)
