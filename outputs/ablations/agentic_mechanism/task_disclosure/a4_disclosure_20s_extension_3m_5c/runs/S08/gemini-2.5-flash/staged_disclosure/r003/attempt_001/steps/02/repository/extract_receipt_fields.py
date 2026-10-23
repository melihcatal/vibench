
import os
from google.cloud import documentai_v1 as documentai

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.
    """
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load image data
    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf" # Adjust mime_type if not PDF (e.g., "image/jpeg", "image/png")
    )

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    # Use the Document AI client to process the document
    result = documentai_client.process_document(request=request)

    document = result.document

    # Initialize extracted fields
    merchant_name = None
    total_amount = None
    tax_amount = None
    items = []

    # Extract entities
    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text
        elif entity.type == "tax_amount":
            tax_amount = entity.mention_text
        elif entity.type == "line_item":
            item_description = None
            item_price = None
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "amount":
                    item_price = prop.mention_text
            if item_description or item_price:
                items.append({"description": item_description, "price": item_price})

    return {
        "merchant": merchant_name,
        "tax": tax_amount,
        "total": total_amount,
        "items": items,
    }

if __name__ == "__main__":
    # Replace with your actual project ID, location, and processor ID
    # You will need to enable the Document AI API and create a "Receipt Parser" processor
    # in the Google Cloud Console.
    project_id = "YOUR_PROJECT_ID"
    location = "YOUR_LOCATION"  # e.g., "us"
    processor_id = "YOUR_PROCESSOR_ID"

    # Replace with the path to your receipt file
    receipt_file_path = "path/to/your/receipt.pdf" # or .jpg, .png etc.

    if not os.path.exists(receipt_file_path):
        print(f"Error: Receipt file not found at {receipt_file_path}")
    else:
        print(f"Extracting fields from {receipt_file_path}...")
        extracted_data = extract_receipt_fields(project_id, location, processor_id, receipt_file_path)

        print("\n--- Extracted Receipt Fields ---")
        print(f"Merchant: {extracted_data['merchant']}")
        print(f"Tax: {extracted_data['tax']}")
        print(f"Total: {extracted_data['total']}")
        print("Items:")
        for item in extracted_data['items']:
            print(f"  - Description: {item['description']}, Price: {item['price']}")
