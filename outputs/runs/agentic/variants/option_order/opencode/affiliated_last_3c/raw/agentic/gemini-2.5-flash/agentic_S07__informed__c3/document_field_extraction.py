from google.cloud import documentai_v1 as documentai
import os


def extract_structured_fields(
    project_id: str, location: str, processor_id: str, file_path: str
):
    """
    Extracts structured fields from a document (e.g., invoice) using a Google Document AI processor.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )  # Assuming PDF

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    extracted_fields = {}
    for entity in result.document.entities:
        # Assuming entities directly represent structured fields
        # For prebuilt processors, entity.type_ would correspond to specific fields like "invoice_id", "total_amount"
        value = (
            entity.normalized_value.text
            if entity.normalized_value
            else entity.text_anchor.text_segments[0].text_content
            if entity.text_anchor.text_segments
            else ""
        )
        extracted_fields[entity.type_] = value

    return extracted_fields


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us"
    # Use a pre-trained processor ID for invoices or receipts
    processor_id = os.environ.get(
        "GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID"
    )  # e.g., "YOUR_INVOICE_PROCESSOR_ID"
    file_path = "path/to/your/invoice.pdf"  # Replace with your document path
    # fields = extract_structured_fields(project_id, location, processor_id, file_path)
    # import json
    # print(json.dumps(fields, indent=2))
