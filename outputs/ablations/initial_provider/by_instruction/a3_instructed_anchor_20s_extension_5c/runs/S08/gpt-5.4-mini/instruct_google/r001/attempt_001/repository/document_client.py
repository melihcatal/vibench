import os
from typing import Any, Dict

from google.cloud import documentai

from document_models import StructuredExtractionRequest, StructuredExtractionResponse


def _client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def _processor_name(project_id: str, location: str, processor_id: str) -> str:
    return _client().processor_path(project_id, location, processor_id)


def extract_with_document_ai(request: StructuredExtractionRequest) -> StructuredExtractionResponse:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.environ["GOOGLE_DOCUMENT_AI_PROCESSOR_ID"]
    with open(request.source_uri, "rb") as fh:
        content = fh.read()
    raw_request = documentai.ProcessRequest(
        name=_processor_name(project_id, location, processor_id),
        raw_document=documentai.RawDocument(content=content, mime_type=request.mime_type),
    )
    result = _client().process_document(request=raw_request)
    fields: Dict[str, Any] = {"text": result.document.text}
    confidence: Dict[str, float] = {"document": result.document.pages[0].confidence if result.document.pages else 0.0}
    return StructuredExtractionResponse(fields=fields, confidence=confidence, raw={"document": result.document._pb.SerializeToString().hex()})
