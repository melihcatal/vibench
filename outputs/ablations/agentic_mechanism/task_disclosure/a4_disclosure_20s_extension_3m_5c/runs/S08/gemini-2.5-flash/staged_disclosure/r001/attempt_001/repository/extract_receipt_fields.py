import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.
    """

    # You would typically store your credentials securely, e.g., using environment variables
    # or Google Cloud's authentication mechanisms.
    # For this example, we assume authentication is already set up in the environment.

    # The Document AI client has a regional endpoint.
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    # Create a Document object
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf" # Or "image/jpeg", "image/png", etc.
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document

    # --- Extracting information ---
    merchant_name = ""
    total_amount = ""
    tax_amount = ""
    items = []

    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.text_anchor.content if entity.text_anchor.content else document.text[entity.text_anchor.text_segments[0].start_index:entity.text_anchor.text_segments[0].end_index]
        elif entity.type == "total_amount":
            total_amount = entity.text_anchor.content if entity.text_anchor.content else document.text[entity.text_anchor.text_segments[0].start_index:entity.text_anchor.text_segments[0].end_index]
        elif entity.type == "tax_amount":
            tax_amount = entity.text_anchor.content if entity.text_anchor.content else document.text[entity.text_anchor.text_segments[0].start_index:entity.text_anchor.text_segments[0].end_index]
        elif entity.type == "line_item":
            item_description = ""
            item_amount = ""
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.text_anchor.content if prop.text_anchor.content else document.text[prop.text_anchor.text_segments[0].start_index:prop.text_anchor.text_segments[0].end_index]
                elif prop.type == "amount":
                    item_amount = prop.text_anchor.content if prop.text_anchor.content else document.text[prop.text_anchor.text_segments[0].start_index:prop.text_anchor.text_segments[0].end_index]
            items.append({"description": item_description, "amount": item_amount})

    return {
        "merchant": merchant_name,
        "tax": tax_amount,
        "total": total_amount,
        "items": items
    }

if __name__ == "__main__":
    # Example usage:
    # Replace with your actual project ID, location, processor ID, and file path
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = "your-processor-id" # Create a "FORM_PARSER" or "RECEIPT_PARSER" processor in Document AI
    RECEIPT_FILE = "path/to/your/receipt.pdf" # or .jpg, .png

    # Ensure you have authenticated with Google Cloud (e.g., `gcloud auth application-default login`)

    # For a receipt processor, you would typically use a specialized processor, e.g., "RECEIPT_PARSER"
    # To create a processor:
    # 1. Go to Google Cloud Console > Document AI
    # 2. Enable the API
    # 3. Create a new processor, choose "Receipt Parser" or "Form Parser"
    # 4. Note down the Processor ID and Location

    if PROJECT_ID == "your-gcp-project-id" or PROCESSOR_ID == "your-processor-id" or RECEIPT_FILE == "path/to/your/receipt.pdf":
        print("Please update PROJECT_ID, LOCATION, PROCESSOR_ID, and RECEIPT_FILE with your actual values.")
    else:
        try:
            extracted_data = extract_receipt_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, RECEIPT_FILE)
            print("Extracted Receipt Data:")
            print(f"Merchant: {extracted_data['merchant']}")
            print(f"Tax: {extracted_data['tax']}")
            print(f"Total: {extracted_data['total']}")
            print("Items:")
            for item in extracted_data['items']:
                print(f"  - Description: {item['description']}, Amount: {item['amount']}")
        except Exception as e:
            print(f"An error occurred: {e}")
