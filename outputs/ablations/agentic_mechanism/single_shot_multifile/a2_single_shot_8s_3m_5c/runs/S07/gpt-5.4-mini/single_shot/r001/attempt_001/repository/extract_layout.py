from google.cloud import vision
from document_client import get_vision_client
from document_models import DocumentLayoutRequest, LayoutElement, LayoutResponse, bbox_to_dict


def extract_layout(request: DocumentLayoutRequest) -> LayoutResponse:
    client = get_vision_client()
    image = vision.Image(content=request.image_bytes)
    response = client.document_text_detection(image=image)
    elements = []
    page = response.full_text_annotation.pages[0] if response.full_text_annotation.pages else None
    if page:
        for block in page.blocks:
            elements.append(LayoutElement(kind="block", text=" ".join(s.text for p in block.paragraphs for s in p.words), bbox=bbox_to_dict(block.bounding_box)))
            for paragraph in block.paragraphs:
                line_text = " ".join(s.text for w in paragraph.words for s in w.symbols)
                elements.append(LayoutElement(kind="line", text=line_text, bbox=bbox_to_dict(paragraph.bounding_box)))
    return LayoutResponse(elements=elements, raw=response)
