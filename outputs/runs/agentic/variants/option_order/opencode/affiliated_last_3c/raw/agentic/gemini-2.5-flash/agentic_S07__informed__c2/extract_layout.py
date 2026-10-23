import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_name
from document_models import DocumentInput, DocumentOutput


def extract_layout_from_document(
    document_input: DocumentInput, project_id: str, location: str, processor_id: str
) -> DocumentOutput:
    """Extracts blocks, lines, or layout elements from a document using Google Document AI."""
    client = get_documentai_client()
    processor_name = get_processor_name(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.content,
        mime_type=document_input.mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    response = client.process_document(request=request)
    document = response.document

    pages_data = []
    for page in document.pages:
        page_dict: Dict[str, Any] = {
            "page_number": page.page_number,
            "dimension": {
                "width": page.dimension.width,
                "height": page.dimension.height,
                "unit": page.dimension.unit,
            },
            "blocks": [],
            "lines": [],
            "tokens": [],
        }

        for block in page.blocks:
            page_dict["blocks"].append(
                {
                    "text_anchor": block.layout.text_anchor.text_segments[0].start_index
                    if block.layout.text_anchor.text_segments
                    else 0
                }
            )
        for line in page.lines:
            page_dict["lines"].append(
                {
                    "text_anchor": line.layout.text_anchor.text_segments[0].start_index
                    if line.layout.text_anchor.text_segments
                    else 0
                }
            )
        for token in page.tokens:
            page_dict["tokens"].append(
                {
                    "text_anchor": token.layout.text_anchor.text_segments[0].start_index
                    if token.layout.text_anchor.text_segments
                    else 0,
                    "detected_break": token.detected_break.type.name
                    if token.detected_break
                    else "NONE",
                }
            )
        pages_data.append(page_dict)

    return DocumentOutput(text=document.text, pages=pages_data)
