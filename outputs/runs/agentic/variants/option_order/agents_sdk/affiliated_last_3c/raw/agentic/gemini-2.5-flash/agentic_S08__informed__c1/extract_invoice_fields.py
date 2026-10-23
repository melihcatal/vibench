import os
from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

    processor_name = documentai_client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    result = documentai_client.process_document(request=request)
    
    document = result.document

    extracted_data = {
        "vendor_name": "",
        "invoice_date": "",
        "total_amount": "",
        "line_items": []
    }

    # Example of parsing fields - actual parsing would be more robust
    for entity in document.entities:
        if entity.type == "supplier_name" and entity.mention_text:
            extracted_data["vendor_name"] = entity.mention_text
        elif entity.type == "invoice_date" and entity.mention_text:
            extracted_data["invoice_date"] = entity.mention_text
        elif entity.type == "total_amount" and entity.mention_text:
            extracted_data["total_amount"] = entity.mention_text
        # Line item extraction would involve iterating through `line_item` entities and their properties
    
    return extracted_data

if __name__ == '__main__':
    # Replace with your actual project_id, location, processor_id, and a test file
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us"
    processor_id = os.getenv("GOOGLE_DOCAI_INVOICE_PROCESSOR_ID") # Pre-trained Invoice Parser
    test_invoice_path = "path/to/your/invoice.pdf" # Replace with a path to a test invoice PDF

    if project_id and processor_id and os.path.exists(test_invoice_path):
        print(f"Extracting fields from {test_invoice_path}...")
        extracted_info = extract_invoice_fields(project_id, location, processor_id, test_invoice_path)
        print("Extracted Invoice Fields:", extracted_info)
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, GOOGLE_DOCAI_INVOICE_PROCESSOR_ID environment variables and ensure test_invoice_path exists.")
        print("Example: GOOGLE_CLOUD_PROJECT='your-project-id' GOOGLE_DOCAI_INVOICE_PROCESSOR_ID='your-processor-id' python extract_invoice_fields.py")
