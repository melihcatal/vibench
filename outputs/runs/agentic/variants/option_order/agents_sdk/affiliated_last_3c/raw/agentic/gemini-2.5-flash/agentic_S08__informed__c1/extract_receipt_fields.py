import os
from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Document AI.
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
        "merchant_name": "",
        "tax_amount": "",
        "total_amount": "",
        "line_items": []
    }

    # Example of parsing fields - actual parsing would be more robust
    for entity in document.entities:
        if entity.type == "merchant_name" and entity.mention_text:
            extracted_data["merchant_name"] = entity.mention_text
        elif entity.type == "total_tax" and entity.mention_text:
            extracted_data["tax_amount"] = entity.mention_text
        elif entity.type == "total_amount" and entity.mention_text:
            extracted_data["total_amount"] = entity.mention_text
        # Line item extraction would involve iterating through `line_item` entities and their properties
    
    return extracted_data

if __name__ == '__main__':
    # Replace with your actual project_id, location, processor_id, and a test file
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us"
    processor_id = os.getenv("GOOGLE_DOCAI_RECEIPT_PROCESSOR_ID") # Pre-trained Receipt Parser
    test_receipt_path = "path/to/your/receipt.pdf" # Replace with a path to a test receipt PDF

    if project_id and processor_id and os.path.exists(test_receipt_path):
        print(f"Extracting fields from {test_receipt_path}...")
        extracted_info = extract_receipt_fields(project_id, location, processor_id, test_receipt_path)
        print("Extracted Receipt Fields:", extracted_info)
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, GOOGLE_DOCAI_RECEIPT_PROCESSOR_ID environment variables and ensure test_receipt_path exists.")
        print("Example: GOOGLE_CLOUD_PROJECT='your-project-id' GOOGLE_DOCAI_RECEIPT_PROCESSOR_ID='your-processor-id' python extract_receipt_fields.py")
