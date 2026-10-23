import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client


def extract_layout_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
):
    """Extracts layout elements (pages, tokens, blocks, etc.) from a document using Google Document AI."""
    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    # Example of accessing layout information
    layout_info = {"text": document.text, "pages": []}
    for page in document.pages:
        page_info = {
            "page_number": page.page_number,
            "dimension": {
                "width": page.dimension.width,
                "height": page.dimension.height,
            },
            "blocks": [],
            "lines": [],
            "tokens": [],
            "form_fields": [],
        }
        for block in page.blocks:
            page_info["blocks"].append(
                {
                    "text": documentai.text_anchor_to_text(
                        block.layout.text_anchor, document.text
                    )
                }
            )
        for line in page.lines:
            page_info["lines"].append(
                {
                    "text": documentai.text_anchor_to_text(
                        line.layout.text_anchor, document.text
                    )
                }
            )
        for token in page.tokens:
            page_info["tokens"].append(
                {
                    "text": documentai.text_anchor_to_text(
                        token.layout.text_anchor, document.text
                    )
                }
            )
        for field in page.form_fields:
            page_info["form_fields"].append(
                {
                    "field_name": documentai.text_anchor_to_text(
                        field.field_name.text_anchor, document.text
                    ),
                    "field_value": documentai.text_anchor_to_text(
                        field.field_value.text_anchor, document.text
                    ),
                }
            )
        layout_info["pages"].append(page_info)
    return layout_info
