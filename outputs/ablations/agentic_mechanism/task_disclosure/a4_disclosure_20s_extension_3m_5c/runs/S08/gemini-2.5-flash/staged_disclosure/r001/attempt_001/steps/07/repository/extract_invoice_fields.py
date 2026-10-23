from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """

    # You can set the api_endpoint to a different Document AI region if needed
    # client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    # client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    # Extract fields
    vendor_name = None
    invoice_date = None
    total_amount = None
    line_items = []

    for entity in document.entities:
        if entity.type == "vendor_name":
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text
        elif entity.type == "line_item":
            line_item_data = {}
            for prop in entity.properties:
                if prop.type == "description":
                    line_item_data["description"] = prop.mention_text
                elif prop.type == "amount":
                    line_item_data["amount"] = prop.mention_text
            if line_item_data:
                line_items.append(line_item_data)

    return {
        "vendor_name": vendor_name,
        "invoice_date": invoice_date,
        "total_amount": total_amount,
        "line_items": line_items,
    }

if __name__ == "__main__":
    # This is a placeholder for demonstration purposes.
    # Replace with your actual project_id, location, processor_id, and invoice file path.
    # Ensure you have authenticated with Google Cloud (e.g., gcloud auth application-default login)
    # and have enabled the Document AI API and created an Invoice Parser processor.
    
    # Example usage:
    # project_id = "your-gcp-project-id"
    # location = "us"  # e.g., "us" or "eu"
    # processor_id = "your-processor-id" # e.g., "xxxxxxxxxxxx" from a 'Invoice Parser' processor
    # invoice_file = "path/to/your/invoice.pdf"

    # For testing, you might need a dummy file or to comment out the actual call.
    # result = extract_invoice_fields(project_id, location, processor_id, invoice_file)
    # print(result)
    print("Please replace placeholders and provide a valid invoice file path to run this script.")
