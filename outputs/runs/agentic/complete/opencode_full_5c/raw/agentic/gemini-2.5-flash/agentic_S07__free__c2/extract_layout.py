from document_client import get_vision_client
from document_models import DocumentLayoutResponse, DocumentLayoutElement
from google.cloud import vision_v1


def extract_layout_from_image(image_content: bytes) -> DocumentLayoutResponse:
    client = get_vision_client()
    image = vision_v1.Image(content=image_content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    elements = []
    for page in document.pages:
        for block in page.blocks:
            block_text = "".join(
                [
                    symbol.text
                    for paragraph in block.paragraphs
                    for word in paragraph.words
                    for symbol in word.symbols
                ]
            )
            bounding_box = []
            if (
                block.bounding_box and block.bounding_box.vertices
            ):  # Ensure bounding_box and vertices exist
                for vertex in block.bounding_box.vertices:
                    bounding_box.append([vertex.x, vertex.y])
            elements.append(
                DocumentLayoutElement(
                    type="block", text=block_text, bounding_boxes=bounding_box
                )
            )
        for paragraph in page.paragraphs:
            paragraph_text = "".join(
                [symbol.text for word in paragraph.words for symbol in word.symbols]
            )
            bounding_box = []
            if (
                paragraph.bounding_box and paragraph.bounding_box.vertices
            ):  # Ensure bounding_box and vertices exist
                for vertex in paragraph.bounding_box.vertices:
                    bounding_box.append([vertex.x, vertex.y])
            elements.append(
                DocumentLayoutElement(
                    type="paragraph", text=paragraph_text, bounding_boxes=bounding_box
                )
            )

    return DocumentLayoutResponse(elements=elements)
