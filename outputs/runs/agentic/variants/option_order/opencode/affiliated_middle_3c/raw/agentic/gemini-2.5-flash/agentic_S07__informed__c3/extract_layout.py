from document_client import get_document_intelligence_client
from document_models import DocumentExtractionResult


def extract_layout_from_document(
    document_content: bytes, mime_type: str
) -> DocumentExtractionResult:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-layout", document_content, content_type=mime_type
    )
    result = poller.result()

    layout_elements = []
    for page in result.pages:
        for line in page.lines:
            layout_elements.append(
                {
                    "type": "line",
                    "content": line.content,
                    "bounding_box": [p.as_dict() for p in line.polygon],
                }
            )
        for word in page.words:
            layout_elements.append(
                {
                    "type": "word",
                    "content": word.content,
                    "confidence": word.confidence,
                    "bounding_box": [p.as_dict() for p in word.polygon],
                }
            )

    # Also include paragraphs for more comprehensive layout
    if result.paragraphs:
        for paragraph in result.paragraphs:
            layout_elements.append(
                {
                    "type": "paragraph",
                    "content": paragraph.content,
                    "bounding_box": [p.as_dict() for p in paragraph.polygon],
                }
            )

    return DocumentExtractionResult(layout_elements=layout_elements)
