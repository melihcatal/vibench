import os
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(file_path: str, project_id: str, location: str, processor_id: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.

    Args:
        file_path (str): The path to the invoice file.
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region (e.g., "us").
        processor_id (str): The ID of your Document AI invoice parser processor.

    Returns:
        dict: A dictionary containing the extracted fields.
    """
    # Google Cloud Document AI client initialization
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf"  # Or "image/jpeg", "image/png", etc.
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_data = {
        "vendor": None,
        "date": None,
        "total": None,
        "line_items": []
    }

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            extracted_data["vendor"] = entity.mention_text
        elif entity.type_ == "invoice_date":
            extracted_data["date"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_data["total"] = entity.mention_text
        elif entity.type_ == "line_item":
            line_item_data = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    line_item_data["description"] = prop.mention_text
                elif prop.type_ == "quantity":
                    line_item_data["quantity"] = prop.mention_text
                elif prop.type_ == "unit_price":
                    line_item_data["unit_price"] = prop.mention_text
                elif prop.type_ == "amount":
                    line_item_data["amount"] = prop.mention_text
            extracted_data["line_items"].append(line_item_data)
    
    return extracted_data

if __name__ == "__main__":
    # Example Usage: Replace with your actual file path, project ID, location, and processor ID
    # For a real-world scenario, you would typically get these values from environment variables
    # or a configuration file.
    invoice_file = "path/to/your/invoice.pdf"  # e.g., "my_invoice.pdf"
    google_cloud_project_id = "your-gcp-project-id"
    google_cloud_location = "us"  # e.g., "us", "eu"
    document_ai_processor_id = "your-processor-id" # e.g., "xxxxxxxxxxxx"

    # Make sure to install the Google Cloud Document AI client library:
    # pip install google-cloud-documentai

    # Authenticate to Google Cloud (e.g., using `gcloud auth application-default login`)
    # For more details, see: https://cloud.google.com/docs/authentication/getting-started

    # try:
    #     extracted_info = extract_invoice_fields(invoice_file, google_cloud_project_id, google_cloud_location, document_ai_processor_id)
    #     print("Extracted Invoice Fields:")
    #     print(f"Vendor: {extracted_info['vendor']}")
    #     print(f"Date: {extracted_info['date']}")
    #     print(f"Total: {extracted_info['total']}")
    #     print("Line Items:")
    #     for item in extracted_info['line_items']:
    #         print(f"  Description: {item.get('description')}, Quantity: {item.get('quantity')}, Unit Price: {item.get('unit_price')}, Amount: {item.get('amount')}")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    print("Please replace the placeholder values for 'invoice_file', 'google_cloud_project_id', 'google_cloud_location', and 'document_ai_processor_id' with your actual details to run this script.")
    print("Uncomment the 'try-except' block and ensure you have authenticated to Google Cloud and installed the necessary libraries.")
