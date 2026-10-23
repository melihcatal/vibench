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
    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf" # Or appropriate mime type for your document
        )
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_data = {
        "vendor_name": "",
        "invoice_date": "",
        "total_amount": "",
        "line_items": []
    }

    # Helper function to extract text from a Document AI entity
    def get_text_from_entity(entity):
        if entity.mention_text:
            return entity.mention_text
        if entity.normalized_value and entity.normalized_value.text:
            return entity.normalized_value.text
        return ""

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            extracted_data["vendor_name"] = get_text_from_entity(entity)
        elif entity.type_ == "invoice_date":
            extracted_data["invoice_date"] = get_text_from_entity(entity)
        elif entity.type_ == "total_amount":
            extracted_data["total_amount"] = get_text_from_entity(entity)
        elif entity.type_ == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    item["description"] = get_text_from_entity(prop)
                elif prop.type_ == "amount":
                    item["amount"] = get_text_from_entity(prop)
                elif prop.type_ == "price":
                    item["price"] = get_text_from_entity(prop)
                elif prop.type_ == "quantity":
                    item["quantity"] = get_text_from_entity(prop)
            if item:
                extracted_data["line_items"].append(item)
    
    return extracted_data

if __name__ == "__main__":
    # Example usage (replace with your actual project, location, processor, and file)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us" # E.g., "us"
    PROCESSOR_ID = "YOUR_INVOICE_PROCESSOR_ID" # Create an Invoice Parser processor in Document AI
    FILE_PATH = "path/to/your/invoice.pdf"

    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up or provide credentials explicitly
    # result = extract_invoice_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    # print(result)
