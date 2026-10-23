from google.cloud import documentai_v1 as documentai
import os


def extract_structured_fields(
    document_content: bytes, mime_type: str = "application/pdf"
) -> dict:
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # Assumes project ID is set in env
    location = "us"  # Or your preferred location
    processor_id = "YOUR_INVOICE_PROCESSOR_ID"  # Replace with your actual Invoice Parser Processor ID
    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
    if processor_id == "YOUR_INVOICE_PROCESSOR_ID":
        raise ValueError(
            "Please replace 'YOUR_INVOICE_PROCESSOR_ID' with your actual Google Document AI Invoice Parser Processor ID."
        )

    documentai_client = documentai.DocumentProcessorServiceClient()

    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = documentai_client.process_document(request=request)
    document = result.document

    # Example of extracting fields - this will vary based on document type and processor
    fields = {}
    for entity in document.entities:
        if entity.type_ == "invoice_id":
            fields["invoice_id"] = entity.mention_text
        elif entity.type_ == "total_amount":
            fields["total_amount"] = entity.mention_text
        # Add more field extractions as needed
    return {"document_text": document.text, "fields": fields}
