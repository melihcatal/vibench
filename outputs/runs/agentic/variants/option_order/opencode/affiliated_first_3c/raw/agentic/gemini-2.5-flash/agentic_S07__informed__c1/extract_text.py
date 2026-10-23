import os
from document_client import get_documentai_client
from document_models import DocumentContent, TextExtractionResult
from google.cloud import documentai_v1 as documentai


def extract_text(
    doc_content: DocumentContent, project_id: str, location: str, processor_id: str
) -> TextExtractionResult:
    client = get_documentai_client()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location-id/processors/processor-id
    # You must create a processor before running this sample.
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(
        content=doc_content.content, mime_type=doc_content.content.mime_type
    )

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    # For a text-only processor, the full text is in the document object
    return TextExtractionResult(text=result.document.text)


if __name__ == "__main__":
    # Example Usage (replace with actual values and file content)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = os.environ.get(
        "GOOGLE_DOCUMENT_AI_OCR_PROCESSOR_ID"
    )  # e.g., "OCR_PROCESSOR_ID"

    if not all([PROJECT_ID, LOCATION, PROCESSOR_ID]):
        print(
            "Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENT_AI_OCR_PROCESSOR_ID environment variables."
        )
    else:
        # Replace with your actual document content and mime type
        with open(
            "path/to/your/document.pdf", "rb"
        ) as image:  # Replace with your document path
            content = image.read()
        doc = DocumentContent(content=content, mime_type="application/pdf")
        text_result = extract_text(doc, PROJECT_ID, LOCATION, PROCESSOR_ID)
        print("Extracted Text:", text_result.text)
