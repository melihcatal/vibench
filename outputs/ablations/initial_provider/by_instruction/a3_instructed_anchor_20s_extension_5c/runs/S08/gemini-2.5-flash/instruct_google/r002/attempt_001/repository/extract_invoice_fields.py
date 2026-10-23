from google.cloud import documentai_v1beta3 as documentai
import os

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": []
    }

    for entity in document.entities:
        if entity.type == "vendor_name":
            extracted_fields["vendor_name"] = entity.mention_text
        elif entity.type == "invoice_date":
            extracted_fields["invoice_date"] = entity.mention_text
        elif entity.type == "total_amount":
            extracted_fields["total_amount"] = entity.mention_text
        elif entity.type == "line_item":
            line_item = {}
            for sub_entity in entity.properties:
                if sub_entity.type == "description":
                    line_item["description"] = sub_entity.mention_text
                elif sub_entity.type == "amount":
                    line_item["amount"] = sub_entity.mention_text
            extracted_fields["line_items"].append(line_item)

    return extracted_fields
