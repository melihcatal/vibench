import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


def extract_invoice_fields(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_data = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": [],
    }

    # Example of how to access fields, actual parsing would be more robust
    for entity in document.entities:
        if entity.type == "vendor_name" and entity.mention_text:
            extracted_data["vendor_name"] = entity.mention_text
        elif entity.type == "invoice_date" and entity.mention_text:
            extracted_data["invoice_date"] = entity.mention_text
        elif entity.type == "total_amount" and entity.mention_text:
            extracted_data["total_amount"] = entity.mention_text
        # More complex logic needed for line items

    return extracted_data


if __name__ == "__main__":
    # Placeholder for actual usage with GOOGLE_APPLICATION_CREDENTIALS set
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = "us"  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_DOCUMENTAI_INVOICE_PROCESSOR_ID"
    )  # e.g., "YOUR_PROCESSOR_ID"

    if not all([project_id, location, processor_id]):
        print(
            "Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENTAI_INVOICE_PROCESSOR_ID environment variables."
        )
    else:
        # Example usage (replace with actual file content and mime type)
        sample_file_content = b"Your invoice content here"
        sample_mime_type = "application/pdf"  # or "image/jpeg"

        # extracted = extract_invoice_fields(project_id, location, processor_id, sample_file_content, sample_mime_type)
        # print(extracted)
        print("Google Document AI client configured for invoice extraction.")
