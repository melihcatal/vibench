import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    # You might need to set up authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # For more details, see: https://cloud.google.com/docs/authentication/production

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf"  # Assuming PDF invoices; adjust if needed
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request)
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
            line_item_data = {}
            for prop in entity.properties:
                if prop.type == "description":
                    line_item_data["description"] = prop.mention_text
                elif prop.type == "amount":
                    line_item_data["amount"] = prop.mention_text
                # Add other line item properties as needed (e.g., quantity, unit_price)
            if line_item_data:
                extracted_data["line_items"].append(line_item_data)

    return extracted_data

