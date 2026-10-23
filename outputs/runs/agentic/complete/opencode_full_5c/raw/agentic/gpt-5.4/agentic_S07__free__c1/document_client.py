from __future__ import annotations

import os
from typing import Any, Dict, List

from google.cloud import documentai_v1 as documentai

from document_models import (
    DocumentRequest,
    OCRTextResult,
    TextSpan,
    load_bytes,
    normalize_whitespace,
)


def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_documentai_processor_path(processor_id_env: str) -> str:
    project_id = get_required_env("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = get_required_env(processor_id_env)
    return get_documentai_client().processor_path(project_id, location, processor_id)


def build_process_request(
    request: DocumentRequest, processor_name: str
) -> documentai.ProcessRequest:
    raw_document = documentai.RawDocument(
        content=load_bytes(request), mime_type=request.mime_type
    )
    options = documentai.ProcessOptions(
        ocr_config=documentai.OcrConfig(language_hints=request.language_hints)
    )
    return documentai.ProcessRequest(
        name=processor_name, raw_document=raw_document, process_options=options
    )


def process_document(
    request: DocumentRequest, processor_id_env: str
) -> documentai.Document:
    client = get_documentai_client()
    processor_name = get_documentai_processor_path(processor_id_env)
    response = client.process_document(
        request=build_process_request(request, processor_name)
    )
    return response.document


def extract_text_spans(document: documentai.Document) -> OCRTextResult:
    spans: List[TextSpan] = []
    full_text = document.text or ""
    for page in document.pages:
        for token in page.tokens:
            anchor = token.layout.text_anchor
            pieces: List[str] = []
            for segment in anchor.text_segments:
                start_index = int(segment.start_index or 0)
                end_index = int(segment.end_index or 0)
                pieces.append(full_text[start_index:end_index])
            token_text = normalize_whitespace("".join(pieces))
            if token_text:
                spans.append(
                    TextSpan(
                        text=token_text,
                        confidence=float(token.layout.confidence or 0.0),
                        page=page.page_number,
                    )
                )
    return OCRTextResult(
        text=normalize_whitespace(full_text),
        spans=spans,
        provider_payload=documentai.Document.to_dict(document),
    )


def text_from_layout(document: documentai.Document, layout: Any) -> str:
    segments = []
    for segment in layout.text_anchor.text_segments:
        start_index = int(segment.start_index or 0)
        end_index = int(segment.end_index or 0)
        segments.append((document.text or "")[start_index:end_index])
    return normalize_whitespace("".join(segments))


def vertices_to_bbox(vertices: List[Any]) -> List[float]:
    bbox: List[float] = []
    for vertex in vertices:
        bbox.extend([float(vertex.x or 0.0), float(vertex.y or 0.0)])
    return bbox


def document_to_dict(document: documentai.Document) -> Dict[str, Any]:
    return documentai.Document.to_dict(document)
