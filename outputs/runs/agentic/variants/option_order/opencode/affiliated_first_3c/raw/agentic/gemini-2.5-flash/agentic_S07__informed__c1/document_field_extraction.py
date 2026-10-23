import os
from document_client import get_documentai_client
from document_models import DocumentContent, FieldExtractionResult
from google.cloud import documentai_v1 as documentai


def extract_fields(
    doc_content: DocumentContent, project_id: str, location: str, processor_id: str
) -> FieldExtractionResult:
    client = get_documentai_client()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location-id/processors/processor-id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(
        content=doc_content.content, mime_type=doc_content.mime_type
    )

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    extracted_fields = {}
    # Example for invoice parser: iterate through entities to find specific fields
    for entity in result.document.entities:
        # Accessing normalized value for structured data, if available
        if (
            entity.type_ == "invoice_date"
            and entity.normalized_value
            and entity.normalized_value.text
        ):
            extracted_fields["invoice_date"] = entity.normalized_value.text
        elif (
            entity.type_ == "total_amount"
            and entity.normalized_value
            and entity.normalized_value.text
        ):
            extracted_fields["total_amount"] = entity.normalized_value.text
        elif entity.type_ == "supplier_name" and entity.mention_text:
            extracted_fields["supplier_name"] = entity.mention_text
        # Add more entity types as needed for the specific processor

    return FieldExtractionResult(fields=extracted_fields)


if __name__ == "main":
    # Example Usage (replace with actual values and file content)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = "us"
    PROCESSOR_ID = os.environ.get(
        "GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID"
    )  # e.g., "invoice-parser"

    if not all([PROJECT_ID, LOCATION, PROCESSOR_ID]):
        print(
            "Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID environment variables."
        )
    else:
        with open(
            "path/to/your/invoice.pdf", "rb"
        ) as invoice_doc:  # Replace with your invoice document path
            content = invoice_doc.read()
        doc = DocumentContent(content=content, mime_type="application/pdf")
        field_result = extract_fields(doc, PROJECT_ID, LOCATION, PROCESSOR_ID)
        print("Extracted Fields:", field_result.fields)
