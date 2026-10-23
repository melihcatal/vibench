from __future__ import annotations

from document_client import build_processor_name, get_documentai_client, get_processor_id, guess_mime_type
from document_models import DocumentRequest, TextExtractionResult, load_bytes, normalize_text
from google.cloud import documentai_v1 as documentai


def extract_text(request: DocumentRequest) -> TextExtractionResult:
    client = get_documentai_client()
    processor_name = build_processor_name(get_processor_id("DOCUMENTAI_OCR_PROCESSOR_ID"))
    raw_document = documentai.RawDocument(
        content=load_bytes(request.file_path),
        mime_type=guess_mime_type(request.file_path, request.mime_type),
    )
    process_request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    result = client.process_document(request=process_request)
    document = result.document
    pages = []
    for page in document.pages:
        page_text = []
        for token in page.tokens:
            anchor = token.layout.text_anchor
            snippets = []
            for segment in anchor.text_segments:
                snippets.append(document.text[int(segment.start_index):int(segment.end_index)])
            if snippets:
                page_text.append("".join(snippets))
        pages.append({"page_number": page.page_number, "text": normalize_text(" ".join(page_text))})
    return TextExtractionResult(
        provider="google_document_ai",
        text=document.text or "",
        pages=pages,
        raw={"mime_type": raw_document.mime_type, "processor": processor_name},
    )
