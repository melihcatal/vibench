from google.cloud import documentai_v1 as documentai
import os

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the invoice parser processor.
        file_path: The path to the invoice document.

    Returns:
        A dictionary containing the extracted fields.
    """

    # Online processing request
    documentai_client = documentai.DocumentProcessorServiceClient()

    name = documentai_client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = documentai_client.process_document(request=request)
    document = result.document

    extracted_fields = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": []
    }

    # Extract fields from the document
    for entity in document.entities:
        if entity.type == "supplier_name":
            extracted_fields["vendor_name"] = entity.mention_text
        elif entity.type == "invoice_date":
            extracted_fields["invoice_date"] = entity.mention_text
        elif entity.type == "total_amount":
            extracted_fields["total_amount"] = entity.mention_text
        elif entity.type == "line_item":
            line_item = {}
            for prop in entity.properties:
                if prop.type == "description":
                    line_item["description"] = prop.mention_text
                elif prop.type == "amount":
                    line_item["amount"] = prop.mention_text
                elif prop.type == "quantity":
                    line_item["quantity"] = prop.mention_text
            if line_item:
                extracted_fields["line_items"].append(line_item)

    return extracted_fields
