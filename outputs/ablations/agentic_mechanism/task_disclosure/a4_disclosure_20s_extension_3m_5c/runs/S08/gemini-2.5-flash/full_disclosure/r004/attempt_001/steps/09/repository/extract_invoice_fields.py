from google.cloud import documentai_v1beta3 as documentai
import os

def extract_invoice_fields(file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = "us"  # Or your preferred region, e.g., "eu"
    processor_id = "your-processor-id" # Create an invoice parser processor in Document AI

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    
    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    mime_type = "application/pdf" # Assuming invoices are PDFs

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
    )

    client = documentai.DocumentProcessorServiceClient()
    result = client.process_document(request=request)

    document = result.document
    extracted_data = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": [],
    }

    for entity in document.entities:
        if entity.type == "supplier_name":
            extracted_data["vendor_name"] = entity.mention_text
        elif entity.type == "invoice_date":
            extracted_data["invoice_date"] = entity.mention_text
        elif entity.type == "total_amount":
            extracted_data["total_amount"] = entity.mention_text
        elif entity.type == "line_item":
            item_data = {}
            for prop in entity.properties:
                if prop.type == "description":
                    item_data["description"] = prop.mention_text
                elif prop.type == "amount":
                    item_data["amount"] = prop.mention_text
                # Add other line item properties as needed
            if item_data:
                extracted_data["line_items"].append(item_data)
    
    return extracted_data
