from typing import List
from google.cloud import vision
from document_client import get_vision_client
from document_models import DocumentLayout, Block, Line, Word, BoundingBox


def extract_layout_from_image(image_path: str) -> List[Block]:
    """
    Extracts layout elements (blocks, lines, words) from a document image.
    """
    client = get_vision_client()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    extracted_blocks = []
    for page in document.pages:
        for block in page.blocks:
            lines = []
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    line_text = "".join([symbol.text for symbol in word.symbols])
                    lines.append(line_text)

            # This is a simplified representation.
            # A more detailed implementation would parse paragraphs and words into lines.
            block_text = "\n".join(lines)

            vertices = block.bounding_box.vertices
            bbox = BoundingBox(
                x1=vertices[0].x, y1=vertices[0].y, x2=vertices[2].x, y2=vertices[2].y
            )

            extracted_blocks.append(
                Block(
                    text=block_text,
                    lines=[],  # Simplified for this example
                    bounding_box=bbox,
                    block_type=vision.Block.BlockType(block.block_type).name,
                )
            )

    return extracted_blocks
