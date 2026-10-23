from google.cloud import documentai_v1 as documentai

from document_client import build_documentai_name, load_config
from document_models import DocumentInput, TextResult, page_text_from_document


def extract_text(document: DocumentInput) -> TextResult:
    config = load_config()
    client = documentai.DocumentProcessorServiceClient()
    name = build_documentai_name(config.gcp_project_id, config.gcp_location, config.gcp_ocr_processor_id or config.gcp_processor_id)
    raw_document = documentai.RawDocument(content=document.content, mime_type=document.mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)
    return TextResult(text=page_text_from_document(response.document))
