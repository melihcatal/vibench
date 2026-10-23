from __future__ import annotations

from document_client import (
    build_process_request,
    document_to_dict,
    get_documentai_client,
    get_processor_name,
)
from document_models import DocumentInput, TextExtractionResult


def extract_text(
    document: DocumentInput, processor_id: str | None = None
) -> TextExtractionResult:
    client = get_documentai_client()
    request = build_process_request(
        document, get_processor_name(processor_id=processor_id)
    )
    response = client.process_document(request=request)
    processed = response.document
    pages = []
    for index, page in enumerate(processed.pages, start=1):
        page_text = []
        for line in page.lines:
            anchor = line.layout.text_anchor
            line_text = (
                "".join(
                    processed.text[
                        s.text_segments[0].start_index : s.text_segments[0].end_index
                    ]
                    for s in [anchor]
                    if getattr(anchor, "text_segments", None)
                )
                if getattr(anchor, "text_segments", None)
                else ""
            )
            page_text.append(line_text)
        pages.append(
            {"page": index, "text": "\n".join(part for part in page_text if part)}
        )
    return TextExtractionResult(
        provider="google_document_ai",
        text=processed.text or "",
        pages=pages,
        raw_response=document_to_dict(processed),
    )
