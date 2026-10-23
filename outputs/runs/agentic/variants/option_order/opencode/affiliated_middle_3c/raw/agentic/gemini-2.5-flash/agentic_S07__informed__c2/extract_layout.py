import os
from typing import Dict, Any, List
from document_client import DocumentAICLient
from document_models import DocumentExtractionRequest, LayoutExtractionResponse
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
GENERAL_PROCESSOR_ID = os.getenv(
    "GOOGLE_DOCUMENT_AI_GENERAL_PROCESSOR_ID", "your-general-processor-id"
)


def extract_layout_from_document(
    request: DocumentExtractionRequest,
) -> LayoutExtractionResponse:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    if not GENERAL_PROCESSOR_ID:
        raise ValueError(
            "GOOGLE_DOCUMENT_AI_GENERAL_PROCESSOR_ID environment variable not set."
        )

    document_ai_client = DocumentAICLient(location=request.location)
    document = document_ai_client.process_document(
        project_id=PROJECT_ID,
        processor_id=request.processor_id
        if request.processor_id != ""
        else GENERAL_PROCESSOR_ID,
        content=request.content,
        mime_type=request.mime_type,
    )

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
                    else 0
                }
            )
        pages_data.append(page_dict)

    # Example of extracting entities if the processor supports it
    entities_data = []
    for entity in document.entities:
        entities_data.append(
            {
                "type": entity.type,
                "mention_text": entity.mention_text,
                "confidence": entity.confidence,
            }
        )

    return LayoutExtractionResponse(pages=pages_data, entities=entities_data)
