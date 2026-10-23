from google.cloud import documentai_v1beta3 as documentai
import os
from document_client import get_documentai_client


def extract_layout_from_document(
    project_id: str, location: str, processor_id: str, file_path: str
):
    """
    Extracts layout elements (pages, blocks, paragraphs, lines, tokens, etc.) from a document using Google Document AI.
    """
    client = get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    layout_info = []
    for page in document.pages:
        page_layout = {
            "page_number": page.page_number,
            "blocks": [
                page.get_text(block.layout.text_anchor) for block in page.blocks
            ],
            "paragraphs": [
                page.get_text(paragraph.layout.text_anchor)
                for paragraph in page.paragraphs
            ],
            "lines": [page.get_text(line.layout.text_anchor) for line in page.lines],
        }
        layout_info.append(page_layout)

    return layout_info
