import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentLayoutExtractionResponse


def extract_layout_from_document(
    file_content: bytes, mime_type: str
) -> DocumentLayoutExtractionResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_CLOUD_DOCUMENTAI_PROCESSOR_ID_LAYOUT", "OCR_PROCESSOR_ID_HERE"
    )  # Replace with your OCR processor ID

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_documentai_client()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    result = client.process_document(request=request)
    document_response = result.document

    layout_elements = []
    # Example: Extracting paragraphs and lines as layout elements
    for paragraph in document_response.paragraphs:
        layout_elements.append(
            {
                "type": "paragraph",
                "text": documentai.get_text_anchor_text(
                    paragraph.layout.text_anchor, document_response.text
                ),
            }
        )

    for page in document_response.pages:
        for line in page.lines:
            layout_elements.append(
                {
                    "type": "line",
                    "text": documentai.get_text_anchor_text(
                        line.layout.text_anchor, document_response.text
                    ),
                }
            )

    return DocumentLayoutExtractionResponse(layout_elements=layout_elements)
