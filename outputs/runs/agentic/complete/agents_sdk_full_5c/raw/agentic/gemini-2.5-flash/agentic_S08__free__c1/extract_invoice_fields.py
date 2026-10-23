from google.cloud import documentai_v1beta3 as documentai
import os

def extract_invoice_fields(document_content: bytes) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us" or "eu"
    processor_id = "INVOICE_PROCESSOR_V1"  # Specific Document AI Invoice Processor

    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(content=document_content, mime_type="application/pdf")

    request = documentai.ProcessRequest(name=name, raw_document=document)
    result = client.process_document(request=request)
    document = result.document

    extracted_data = {}
    for entity in document.entities:
        if entity.type_ == "vendor_name":
            extracted_data["vendor_name"] = entity.mention_text
        elif entity.type_ == "invoice_date":
            extracted_data["invoice_date"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_data["total_amount"] = entity.mention_text
        elif entity.type_ == "line_item":
            if "line_items" not in extracted_data:
                extracted_data["line_items"] = []
            line_item_data = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    line_item_data["description"] = prop.mention_text
                elif prop.type_ == "amount":
                    line_item_data["amount"] = prop.mention_text
            extracted_data["line_items"].append(line_item_data)
            
    return extracted_data
