import os
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The location of the processor (e.g., "us").
        processor_id (str): The ID of the Invoice Parser processor.
        file_path (str): The path to the invoice file (PDF, PNG, TIFF, etc.).

    Returns:
        dict: A dictionary containing extracted fields (vendor, date, total, line_items).
    """
    # Instantiates a client
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image_file:
        content = image_file.read()

    # Configure the process request
    document = documentai.RawDocument(content=content, mime_type="application/pdf") # Assuming PDF, adjust as needed

    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    # Recognizes text entities in the input document
    result = documentai_client.process_document(request=request)
    document_proto = result.document

    extracted_data = {
        "vendor": None,
        "date": None,
        "total": None,
        "line_items": []
    }

    for entity in document_proto.entities:
        if entity.type == "supplier_name":
            extracted_data["vendor"] = entity.mention_text
        elif entity.type == "invoice_date":
            extracted_data["date"] = entity.mention_text
        elif entity.type == "total_amount":
            extracted_data["total"] = entity.mention_text
        elif entity.type == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type == "description":
                    item["description"] = prop.mention_text
                elif prop.type == "quantity":
                    item["quantity"] = prop.mention_text
                elif prop.type == "unit_price":
                    item["unit_price"] = prop.mention_text
                elif prop.type == "line_item_amount":
                    item["amount"] = prop.mention_text
            if item:
                extracted_data["line_items"].append(item)
    
    return extracted_data
