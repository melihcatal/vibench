from google.cloud import vision

from document_client import vision_client
from document_models import DocumentRequest, LayoutResponse


def extract_layout(request: DocumentRequest) -> LayoutResponse:
    client = vision_client()
    with open(request.image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    result = client.document_text_detection(image=image)
    blocks = []
    lines = []
    tables = []
    for page in (
        result.full_text_annotation.pages if result.full_text_annotation else []
    ):
        for block in page.blocks:
            blocks.append(block.bounding_box.vertices)
            for paragraph in block.paragraphs:
                line_text = " ".join(
                    symbol.text for word in paragraph.words for symbol in word.symbols
                )
                lines.append(line_text)
    return LayoutResponse(blocks=blocks, lines=lines, tables=tables)
