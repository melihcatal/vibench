import json
from google.cloud import documentai_v1 as documentai

def extract_receipt_fields(image_bytes):
    # Initialize Document AI client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    client = documentai.DocumentProcessorServiceClient()
    # Receipt processor resource (replace with real processor ID)
    processor_name = "projects/PROJECT_ID/locations/us-central1/processors/RECEIPT_PROCESSOR_ID"
    raw_document = documentai.RawDocument(content=image_bytes, mime_type="application/pdf")
    document = documentai.Document(raw_document=raw_document)
    response = client.process_document(name=processor_name, document=document)

    fields = {}
    for ent in response.document.entities:
        if ent.type_ == "MERCHANT":
            fields["merchant"] = ent.mention_text
        elif ent.type_ == "AMOUNT" and ent.property.get("label").value == "SUBTOTAL":
            fields["subtotal"] = float(ent.mention_text.replace(",", ""))
        elif ent.type_ == "AMOUNT" and ent.property.get("label").value == "TAX":
            fields["tax"] = float(ent.mention_text.replace(",", ""))
        elif ent.type_ == "LINE_ITEM":
            if "items" not in fields:
                fields["items"] = []
            fields["items"].append({
                "description": ent.property.get("description").value,
                "price": float(ent.mention_text.replace(",", "")),
                "quantity": int(ent.property.get("quantity").value)
            })
    return fields
