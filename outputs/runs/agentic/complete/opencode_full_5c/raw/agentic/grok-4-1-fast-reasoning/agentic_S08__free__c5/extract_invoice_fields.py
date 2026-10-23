import os
from google.cloud import documentai_v1 as documentai
from document_models import InvoiceFields

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us"
PROCESSOR_ID = "61b5c4031f39a88b1bd8dadd"


def extract_invoice_fields(document_bytes: bytes) -> InvoiceFields:
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=document_bytes, mime_type="application/pdf"
        ),
    )
    result = client.process_document(request=request)
    doc = result.document
    entities = {}
    for entity in doc.entities:
        entities[entity.type_] = entity.mention_text
    vendor = entities.get("supplier_name", "")
    date = entities.get("invoice_date", "")
    total_str = entities.get("invoice_total", "0").replace(",", "").replace("$", "")
    total = float(total_str) if total_str else 0.0
    line_items = []
    return {"vendor": vendor, "date": date, "total": total, "line_items": line_items}
