
import os
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region (e.g., "us").
        processor_id (str): The ID of the invoice parser processor.
        file_path (str): The path to the invoice file (PDF, TIFF, JPEG, PNG).
    """

    # Initialize client
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Determine the mime_type based on the file extension
    mime_type = ""
    if file_path.endswith(".pdf"):
        mime_type = "application/pdf"
    elif file_path.endswith(".tiff") or file_path.endswith(".tif"):
        mime_type = "image/tiff"
    elif file_path.endswith(".jpeg") or file_path.endswith(".jpg"):
        mime_type = "image/jpeg"
    elif file_path.endswith(".png"):
        mime_type = "image/png"
    else:
        raise ValueError("Unsupported file type. Please provide a PDF, TIFF, JPEG, or PNG file.")

    # Create raw document object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    # Process the document
    result = documentai_client.process_document(request=request)
    document = result.document

    # Extract fields
    vendor_name = None
    invoice_date = None
    total_amount = None
    line_items = []

    for entity in document.entities:
        if entity.type == "vendor_name":
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text # This will be the raw text including currency
        elif entity.type == "line_item":
            item = {}
            for sub_entity in entity.properties:
                if sub_entity.type == "description":
                    item["description"] = sub_entity.mention_text
                elif sub_entity.type == "quantity":
                    item["quantity"] = sub_entity.mention_text
                elif sub_entity.type == "unit_price":
                    item["unit_price"] = sub_entity.mention_text
                elif sub_entity.type == "amount":
                    item["amount"] = sub_entity.mention_text
            if item:
                line_items.append(item)

    return {
        "vendor_name": vendor_name,
        "invoice_date": invoice_date,
        "total_amount": total_amount,
        "line_items": line_items,
    }

