import os
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """

    # Fully qualified processor name
    # Format: projects/{project_id}/locations/{location}/processors/{processor_id}
    processor_name = documentai.DocumentProcessorServiceClient.common_processor_path(
        project_id, location, processor_id
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Create a Document object
    document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF, adjust if needed

    # Configure the process request
    request = documentai.ProcessRequest(name=processor_name, raw_document=document)

    # Initialize client that will be used to send requests
    client = documentai.DocumentProcessorServiceClient()

    # Process the document
    result = client.process_document(request=request)

    # For a general processor, the response type is Document
    document = result.document

    vendor = None
    invoice_date = None
    total_amount = None
    line_items = []

    # Extract fields based on Document AI parsing
    for entity in document.entities:
        if entity.type == "vendor_name":
            vendor = entity.mention_text
        elif entity.type == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text
        elif entity.type == "line_item":
            line_item_data = {}
            for prop in entity.properties:
                if prop.type == "product_description":
                    line_item_data["description"] = prop.mention_text
                elif prop.type == "quantity":
                    line_item_data["quantity"] = prop.mention_text
                elif prop.type == "unit_price":
                    line_item_data["unit_price"] = prop.mention_text
                elif prop.type == "amount":
                    line_item_data["amount"] = prop.mention_text
            if line_item_data:
                line_items.append(line_item_data)

    return {
        "vendor": vendor,
        "date": invoice_date,
        "total": total_amount,
        "line_items": line_items,
    }

