import os
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(invoice_bytes):
    client = documentai.DocumentProcessorServiceClient()
    processor_id = os.getenv("INVOICE_PROCESSOR_ID")
    name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/processors/{processor_id}"
    raw_document = documentai.RawDocument(content=invoice_bytes, mime_type="application/pdf")
    response = client.process_document(name=name, raw_document=raw_document)
    document = response.document
    vendor = None
    invoice_date = None
    total = None
    line_items = []
    for entity in document.entities:
        type_ = entity.type_
        if type_ == "VENDOR":
            vendor = entity.merged_entity.value
        elif type_ == "DATE":
            invoice_date = entity.normalized_value.date_value
        elif type_ == "AMOUNT_OF_MONEY":
            if total is None:
                total = entity.normalized_value.float_value
        elif type_ == "LINE_ITEM":
            line_items.append({
                "description": entity.merged_entity.value,
                "quantity": entity.properties.get("Quantity", {}).normalized_value.float_value,
                "unit_price": entity.properties.get("UnitPrice", {}).normalized_value.float_value,
                "total": entity.properties.get("LineTotal", {}).normalized_value.float_value,
            })
    return {
        "vendor": vendor,
        "date": invoice_date,
        "total": total,
        "line_items": line_items,
    }
