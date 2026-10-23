import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    extracted_data = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": []
    }

    for entity in document.entities:
        if entity.type == "supplier_name":
            extracted_data["vendor_name"] = entity.mention_text
        elif entity.type == "invoice_date":
            extracted_data["invoice_date"] = entity.mention_text
        elif entity.type == "total_amount":
            extracted_data["total_amount"] = entity.mention_text
        elif entity.type == "line_item":
            line_item = {}
            for prop in entity.properties:
                if prop.type == "description":
                    line_item["description"] = prop.mention_text
                elif prop.type == "amount":
                    line_item["amount"] = prop.mention_text
            if line_item:
                extracted_data["line_items"].append(line_item)
    return extracted_data
