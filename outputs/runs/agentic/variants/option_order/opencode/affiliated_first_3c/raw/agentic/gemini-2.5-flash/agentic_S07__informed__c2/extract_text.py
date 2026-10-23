from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
from document_client import get_documentai_client
from document_models import DocumentRequest


def extract_text(request: DocumentRequest) -> str:
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
    return result.document.text
