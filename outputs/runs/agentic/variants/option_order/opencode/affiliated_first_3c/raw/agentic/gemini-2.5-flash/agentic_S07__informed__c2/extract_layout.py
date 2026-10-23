from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentRequest, LayoutExtractionResponse


def extract_layout(request: DocumentRequest) -> LayoutExtractionResponse:
    client = get_documentai_client()
    processor_name = client.processor_path(
        request.project_id, request.location, request.processor_id
    )

    raw_document = documentai.RawDocument(
        content=request.file_content,
        mime_type=request.mime_type,
    )
    request_options = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request_options)

    # Example: Extracting pages and their dimensions
    pages_data = []
    for page in result.document.pages:
        pages_data.append(
            {
                "page_number": page.page_number,
                "dimension": {
                    "width": page.dimension.width,
                    "height": page.dimension.height,
                    "unit": page.dimension.unit,
                },
                "blocks": [],  # Placeholder for more detailed layout elements
            }
        )

    return LayoutExtractionResponse(text=result.document.text, pages=pages_data)
