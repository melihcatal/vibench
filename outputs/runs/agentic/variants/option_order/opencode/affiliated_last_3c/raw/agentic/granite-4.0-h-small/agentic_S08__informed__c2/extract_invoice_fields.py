import os
import json
from google.cloud import documentai


def extract_invoice_fields(pdf_bytes):
    # Authenticate using GOOGLE_APPLICATION_CREDENTIALS env variable
    client = documentai.DocumentProcessorServiceClient()
    # Assuming processor ID is set in env var DOCUMENTAI_INVOICE_PROCESSOR_ID
    processor_id = os.getenv("DOCUMENTAI_INVOICE_PROCESSOR_ID")
    name = client.processor_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), "us-central1", processor_id
    )
    # Prepare the document
    raw_document = documentai.RawDocument(
        content=pdf_bytes, mime_type="application/pdf"
    )
    # Request
    response = client.process_document(name=name, raw_document=raw_document)
    # Parse entities (example handling)
    document = response.document
    vendor = ""
    date = ""
    total = ""
    line_items = []
    for entity in document.entities:
        type_ = entity.type_
        text = document.text.content[
            entity.text_anchor.start_index : entity.text_anchor.end_index
        ]
        if type_ == "VENDOR_NAME":
            vendor = text
        elif type_ == "INVOICE_DATE":
            date = text
        elif type_ == "TOTAL_AMOUNT":
            total = text
        elif type_ == "LINE_ITEM_DESCRIPTION":
            # simplistic line item extraction
            line_items.append({"description": text})
    return {"vendor": vendor, "date": date, "total": total, "line_items": line_items}
