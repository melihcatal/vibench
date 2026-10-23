from google.cloud import documentai_v1 as documentai
import os

def extract_receipt_fields(file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.

    Args:
        file_path: The path to the receipt file.

    Returns:
        A dictionary containing the extracted fields.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")  # Replace with your GCP project ID
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us" or "eu"
    processor_id = os.getenv("DOCUMENT_AI_PROCESSOR_ID", "your-receipt-processor-id") # e.g., for Receipt Parser V1

    # Create a Document AI client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf" if file_path.endswith(".pdf") else "image/jpeg",
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_data = {
        "merchant": None,
        "tax": None,
        "total": None,
        "items": []
    }

    # Extract fields from the document
    for entity in document.entities:
        if entity.type == "merchant_name" and entity.mention_text:
            extracted_data["merchant"] = entity.mention_text
        elif entity.type == "total_amount" and entity.mention_text:
            extracted_data["total"] = entity.mention_text
        elif entity.type == "tax_amount" and entity.mention_text:
            extracted_data["tax"] = entity.mention_text
        elif entity.type == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type == "description" and prop.mention_text:
                    item["description"] = prop.mention_text
                elif prop.type == "amount" and prop.mention_text:
                    item["amount"] = prop.mention_text
                elif prop.type == "quantity" and prop.mention_text:
                    item["quantity"] = prop.mention_text
            if item:
                extracted_data["items"].append(item)

    return extracted_data
