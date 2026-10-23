import json
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(pdf_bytes):
    # Initialize Document AI client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    client = documentai.DocumentProcessorServiceClient()
    # Construct the resource path for the processor (e.g., invoice parser)
    processor_name = "projects/PROJECT_ID/locations/us-central1/processors/INVOICE_PROCESSOR_ID"
    # Prepare the document payload
    raw_document = documentai.RawDocument(content=pdf_bytes, mime_type="application/pdf")
    document = documentai.Document(raw_document=raw_document)
    # Send request to Document AI
    response = client.process_document(name=processor_name, document=document)

    # Parse response into structured fields
    fields = {}
    for ent in response.document.entities:
        if ent.type_ == "VENDOR":
            fields["vendor"] = ent.mention_text
        elif ent.type_ == "DATE":
            fields["date"] = ent.mention_text
        elif ent.type_ == "AMOUNT" and ent.property.get("label").value == "TOTAL":
            fields["total"] = float(ent.mention_text.replace(",", ""))
        elif ent.type_ == "LINE_ITEM":
            # Accumulate line items
            if "line-items" not in fields:
                fields["line-items"] = []
            fields["line-items"].append({
                "description": ent.property.get("description").value,
                "amount": float(ent.mention_text.replace(",", ""))
            })
    return fields
