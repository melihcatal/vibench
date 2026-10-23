import os
from document_client import DocumentAIClient
from document_models import DocumentResponse, DocumentPage
from google.cloud import documentai_v1 as documentai


def extract_plain_text(
    file_content: bytes, mime_type: str, processor_id: str
) -> DocumentResponse:
    """
    Extracts plain text from a scanned document image using Google Document AI.
    """
    client = DocumentAIClient()
    document = client.process_document(file_content, mime_type, processor_id)

    pages = []
    for page in document.pages:
        page_text = ""
        for block in page.blocks:
            if block.layout.text_anchor.text_segments:
                for segment in block.layout.text_anchor.text_segments:
                    start_index = int(segment.start_index)
                    end_index = int(segment.end_index)
                    page_text += document.text[start_index:end_index] + " "

        pages.append(
            DocumentPage(
                page_number=page.page_number,
                image_width=page.dimension.width,
                image_height=page.dimension.height,
                text=page_text.strip(),
                blocks=[],  # Not populating for plain text extraction
                tables=[],
                form_fields=[],
            )
        )

    return DocumentResponse(text=document.text, pages=pages, entities=[])
