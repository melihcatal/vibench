import os
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    # Initialize Document AI client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g., "projects/{project_id}/locations/{location}/processors/{processor_id}"
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf"  # Assuming PDF invoices, adjust if needed
        )
    )

    result = client.process_document(request=request)
    document = result.document

    vendor_name = None
    invoice_date = None
    total_amount = None
    line_items = []

    # Extract fields
    for entity in document.entities:
        if entity.type == "vendor_name":
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text
        elif entity.type == "line_item":
            item_description = None
            item_amount = None
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "amount":
                    item_amount = prop.mention_text
            if item_description or item_amount:
                line_items.append({"description": item_description, "amount": item_amount})

    return {
        "vendor_name": vendor_name,
        "invoice_date": invoice_date,
        "total_amount": total_amount,
        "line_items": line_items
    }

if __name__ == "__main__":
    # Example usage (replace with your actual project details and file path)
    PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = "YOUR_INVOICE_PROCESSOR_ID"  # Create an Invoice Parser processor in Document AI
    FILE_PATH = "path/to/your/invoice.pdf"

    if PROJECT_ID == "YOUR_GOOGLE_CLOUD_PROJECT_ID" or PROCESSOR_ID == "YOUR_INVOICE_PROCESSOR_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' and 'YOUR_INVOICE_PROCESSOR_ID' with your actual Google Cloud project ID and Document AI processor ID.")
        print("Also, update 'FILE_PATH' to the path of your invoice PDF.")
    else:
        try:
            extracted_data = extract_invoice_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
            print("Extracted Invoice Fields:")
            print(f"Vendor Name: {extracted_data['vendor_name']}")
            print(f"Invoice Date: {extracted_data['invoice_date']}")
            print(f"Total Amount: {extracted_data['total_amount']}")
            print("Line Items:")
            for item in extracted_data['line_items']:
                print(f"  Description: {item['description']}, Amount: {item['amount']}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please ensure you have authenticated to Google Cloud and that the Document AI API is enabled.")
            print("Also, verify that the processor ID and file path are correct.")
