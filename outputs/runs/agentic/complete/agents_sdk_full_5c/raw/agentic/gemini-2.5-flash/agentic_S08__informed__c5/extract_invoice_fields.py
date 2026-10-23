import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf" # or "image/jpeg", "image/png"
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    # Extract fields (simplified for brevity)
    extracted_data = {}
    for entity in document.entities:
        if entity.type_ == "vendor_name":
            extracted_data["vendor_name"] = entity.mention_text
        elif entity.type_ == "invoice_date":
            extracted_data["invoice_date"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_data["total_amount"] = entity.mention_text
        # More complex parsing needed for line items
        # For simplicity, we'll just show some main fields.
        # Line items would typically involve iterating through entities of type 'line_item'
        # and then their properties like 'description', 'amount', 'quantity'.
    
    return extracted_data

if __name__ == '__main__':
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us") # e.g., "us"
    PROCESSOR_ID = os.environ.get("GOOGLE_DOCUMENTAI_INVOICE_PROCESSOR_ID")
    INVOICE_FILE = "path/to/your/invoice.pdf" # Replace with actual path

    if not all([PROJECT_ID, PROCESSOR_ID]):
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENTAI_INVOICE_PROCESSOR_ID environment variables.")
    else:
        # Create a dummy file for demonstration if it doesn't exist
        if not os.path.exists(INVOICE_FILE):
            print(f"Dummy file not found at {INVOICE_FILE}. Skipping extraction demo.")
            print("Please create a dummy invoice.pdf or provide a real one to run this example.")
        else:
            print(f"Extracting fields from {INVOICE_FILE}...")
            fields = extract_invoice_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, INVOICE_FILE)
            print("Extracted Invoice Fields:", fields)
