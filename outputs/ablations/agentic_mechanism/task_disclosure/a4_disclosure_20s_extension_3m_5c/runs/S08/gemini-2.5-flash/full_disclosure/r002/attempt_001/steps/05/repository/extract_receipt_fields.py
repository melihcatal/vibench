import os
from google.cloud import documentai_v1 as documentai

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region to run the processor (e.g., "us").
        processor_id (str): The ID of the receipt processor to use.
        file_path (str): The path to the receipt file (e.g., image, PDF).

    Returns:
        dict: A dictionary containing extracted fields like merchant, tax, total, and items.
              Returns an empty dictionary if extraction fails or no relevant fields are found.
    """
    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image_file:
        content = image_file.read()

    document = documentai.RawDocument(content=content, mime_type="application/pdf") # Assuming PDF, adjust if needed

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=document)

    # Recognizes text entities in the document
    result = client.process_document(request=request)
    document = result.document

    extracted_data = {
        "merchant": None,
        "tax": None,
        "total": None,
        "items": []
    }

    for entity in document.entities:
        if entity.type_ == "merchant_name":
            extracted_data["merchant"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_data["total"] = entity.mention_text
        elif entity.type_ == "tax_amount":
            extracted_data["tax"] = entity.mention_text
        elif entity.type_ == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "amount":
                    item["amount"] = prop.mention_text
            if item:
                extracted_data["items"].append(item)

    return extracted_data

