import os
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_data = {
        "vendor_name": "",
        "invoice_date": "",
        "total_amount": "",
        "line_items": []
    }

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            extracted_data["vendor_name"] = entity.mention_text
        elif entity.type_ == "invoice_date":
            extracted_data["invoice_date"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_data["total_amount"] = entity.mention_text
        elif entity.type_ == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "quantity":
                    item["quantity"] = prop.mention_text
                elif prop.type_ == "unit_price":
                    item["unit_price"] = prop.mention_text
                elif prop.type_ == "amount":
                    item["amount"] = prop.mention_text
            if item:
                extracted_data["line_items"].append(item)
    
    return extracted_data

if __name__ == '__main__':
    # This is a placeholder for actual credential/config loading
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = "us" # e.g., "us"
    PROCESSOR_ID = os.environ.get("DOCUMENT_AI_INVOICE_PROCESSOR_ID") # e.g., "YOUR_PROCESSOR_ID"
    # Make sure to replace 'invoice.pdf' with a real file path for testing
    # and have GOOGLE_APPLICATION_CREDENTIALS set or similar authentication configured.
    if PROJECT_ID and PROCESSOR_ID:
        try:
            # Example usage - replace with a real PDF file
            # result = extract_invoice_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, "path/to/your/invoice.pdf")
            # print("Extracted Invoice Fields:", result)
            print("To run, provide a PDF file path and ensure GOOGLE_CLOUD_PROJECT_ID and DOCUMENT_AI_INVOICE_PROCESSOR_ID environment variables are set.")
        except Exception as e:
            print(f"Error extracting invoice fields: {e}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and DOCUMENT_AI_INVOICE_PROCESSOR_ID environment variables.")
