from typing import List
from google.cloud import documentai

from document_client import get_document_ai_client, get_settings
from document_models import ExtractedInvoice, InvoiceLineItem


def extract_invoice_fields(file_path: str, mime_type: str) -> ExtractedInvoice:
    """
    Extracts structured data from an invoice document using Google Cloud Document AI.
    """
    client = get_document_ai_client()
    settings = get_settings()

    name = client.processor_path(
        settings.GOOGLE_PROJECT_ID, settings.GOOGLE_LOCATION, settings.GOOGLE_PROCESSOR_ID
    )

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    doc = result.document

    # For a full list of fields, see:
    # https://cloud.google.com/document-ai/docs/processors-list#processor_invoice-parser
    
    extracted_data = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": [],
        "raw_fields": {}
    }

    for entity in doc.entities:
        key = entity.type_
        value = entity.mention_text
        confidence = entity.confidence
        
        extracted_data["raw_fields"][key] = {"value": value, "confidence": confidence}

        if key == "supplier_name":
            extracted_data["vendor_name"] = value
        elif key == "invoice_date":
            extracted_data["invoice_date"] = value
        elif key == "total_amount":
            try:
                extracted_data["total_amount"] = float(value.replace("$", "").replace(",",""))
            except (ValueError, TypeError):
                extracted_data["total_amount"] = None
        elif key == "line_item" and entity.entities:
            line_item = {}
            for sub_entity in entity.entities:
                if sub_entity.type_ == "line_item/description":
                    line_item["description"] = sub_entity.mention_text
                elif sub_entity.type_ == "line_item/amount":
                    try:
                        line_item["amount"] = float(sub_entity.mention_text)
                    except (ValueError, TypeError):
                        pass
            if line_item:
                 extracted_data["line_items"].append(InvoiceLineItem(**line_item))


    return ExtractedInvoice(**extracted_data)
