
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    processor_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_data = {
        "vendor_name": "",
        "invoice_date": "",
        "total_amount": "",
        "line_items": []
    }

    def _get_text_from_span(document, text_anchor):
        if not text_anchor.text_segments:
            return ""
        text_segment = text_anchor.text_segments[0]
        start_index = text_segment.start_index
        end_index = text_segment.end_index
        return document.text[start_index:end_index]

    for entity in document.entities:
        if entity.type == "vendor_name":
            extracted_data["vendor_name"] = _get_text_from_span(document, entity.text_anchor)
        elif entity.type == "invoice_date":
            extracted_data["invoice_date"] = _get_text_from_span(document, entity.text_anchor)
        elif entity.type == "total_amount":
            extracted_data["total_amount"] = _get_text_from_span(document, entity.text_anchor)
        elif entity.type == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type == "description":
                    item["description"] = _get_text_from_span(document, prop.text_anchor)
                elif prop.type == "amount":
                    item["amount"] = _get_text_from_span(document, prop.text_anchor)
                elif prop.type == "quantity":
                    item["quantity"] = _get_text_from_span(document, prop.text_anchor)
            if item:
                extracted_data["line_items"].append(item)

    return extracted_data

if __name__ == '__main__':
    # Example usage placeholder:
    # Set your Google Cloud project details and processor ID
    # PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    # LOCATION = "us" # e.g., "us"
    # PROCESSOR_ID = os.getenv("DOCUMENTAI_INVOICE_PROCESSOR_ID") # e.g., "YOUR_PROCESSOR_ID"
    # FILE_PATH = "path/to/your/invoice.pdf"

    # if PROJECT_ID and PROCESSOR_ID and os.path.exists(FILE_PATH):
    #     invoice_data = extract_invoice_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    #     print("Extracted Invoice Data:", invoice_data)
    # else:
    #     print("Please set GCP_PROJECT_ID, DOCUMENTAI_INVOICE_PROCESSOR_ID environment variables and ensure FILE_PATH exists.")
    pass
