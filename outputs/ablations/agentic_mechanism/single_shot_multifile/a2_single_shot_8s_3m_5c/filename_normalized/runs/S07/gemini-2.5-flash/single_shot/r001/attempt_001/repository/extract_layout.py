from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_project_id, get_location, DOCUMENT_AI_PROCESSOR_OCR
from document_models import LayoutBlock

def extract_layout_elements(document_bytes: bytes, mime_type: str) -> list[LayoutBlock]:
    project_id = get_project_id()
    location = get_location()
    processor_id = DOCUMENT_AI_PROCESSOR_OCR
    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)
    document = response.document
    layout_blocks: list[LayoutBlock] = []
    def convert_bounding_poly(bounding_poly) -> list[list[int]]:
        if not bounding_poly or not bounding_poly.vertices:
            return []
        return [[vertex.x, vertex.y] for vertex in bounding_poly.vertices]
    for page in document.pages:
        for paragraph in page.paragraphs:
            layout_blocks.append(LayoutBlock(
                text=paragraph.layout.text_anchor.text_segments[0].text_content if paragraph.layout.text_anchor.text_segments else "",
                bounding_boxes=convert_bounding_poly(paragraph.layout.bounding_poly),
                block_type="paragraph",
                confidence=paragraph.layout.confidence
            ))
        for line in page.lines:
            layout_blocks.append(LayoutBlock(
                text=line.layout.text_anchor.text_segments[0].text_content if line.layout.text_anchor.text_segments else "",
                bounding_boxes=convert_bounding_poly(line.layout.bounding_poly),
                block_type="line",
                confidence=line.layout.confidence
            ))
        for token in page.tokens:
            layout_blocks.append(LayoutBlock(
                text=token.layout.text_anchor.text_segments[0].text_content if token.layout.text_anchor.text_segments else "",
                bounding_boxes=convert_bounding_poly(token.layout.bounding_poly),
                block_type="word",
                confidence=token.layout.confidence
            ))
    return layout_blocks