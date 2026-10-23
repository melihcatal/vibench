import os
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """

    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf"  # Assuming PDF invoices
        )
    )

    result = client.process_document(request=request)
    document = result.document

    vendor_name = ""
    invoice_date = ""
    total_amount = ""
    line_items = []

    for entity in document.entities:
        if entity.type == "supplier_name":
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text
        elif entity.type == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type == "description":
                    item["description"] = prop.mention_text
                elif prop.type == "quantity":
                    item["quantity"] = prop.mention_text
                elif prop.type == "unit_price":
                    item["unit_price"] = prop.mention_text
                elif prop.type == "amount":
                    item["amount"] = prop.mention_text
            if item:
                line_items.append(item)

    return {
        "vendor_name": vendor_name,
        "invoice_date": invoice_date,
        "total_amount": total_amount,
        "line_items": line_items
    }

if __name__ == "__main__":
    # Example Usage:
    # Set environment variables or replace with your actual values
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
    # PROJECT_ID = "your-gcp-project-id"
    # LOCATION = "us"  # e.g., "us" or "eu"
    # PROCESSOR_ID = "your-processor-id" # Create an Invoice Parser processor in Document AI

    # For demonstration purposes, using placeholder values.
    # In a real scenario, you would retrieve these from environment variables or a configuration.
    PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    LOCATION = os.environ.get("GCP_LOCATION", "us")
    PROCESSOR_ID = os.environ.get("GCP_PROCESSOR_ID", "your-processor-id")
    INVOICE_FILE = "path/to/your/invoice.pdf" # Replace with your invoice file path

    if PROJECT_ID == "your-gcp-project-id" or PROCESSOR_ID == "your-processor-id":
        print("Please set your GCP_PROJECT_ID, GCP_LOCATION, and GCP_PROCESSOR_ID environment variables, or update the placeholder values in the script.")
        print("Also, ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication.")
    else:
        print(f"Extracting fields from {INVOICE_FILE} using Document AI...")
        extracted_data = extract_invoice_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, INVOICE_FILE)
        print("Extracted Data:")
        print(f"Vendor Name: {extracted_data['vendor_name']}")
        print(f"Invoice Date: {extracted_data['invoice_date']}")
        print(f"Total Amount: {extracted_data['total_amount']}")
        print("Line Items:")
        for item in extracted_data['line_items']:
            print(f"  Description: {item.get('description', '')}, Quantity: {item.get('quantity', '')}, Unit Price: {item.get('unit_price', '')}, Amount: {item.get('amount', '')}")
