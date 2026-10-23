from google.cloud import vision
from document_client import get_document_client
from document_models import Block, Line, Word, BoundingBox, Point


def extract_document_layout(image_path: str) -> list[Block]:
    """
    Extracts layout elements (blocks, lines, words) from a document image
    using Google Cloud Vision API.
    """
    client = get_document_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Provider-specific feature for layout extraction
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    document_blocks = []
    annotation = response.full_text_annotation
    for page in annotation.pages:
        for block in page.blocks:
            block_text = ""
            block_lines = []
            block_bbox = BoundingBox(
                vertices=[Point(v.x, v.y) for v in block.bounding_box.vertices]
            )

            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    line_text = ""
                    word_symbols = "".join([symbol.text for symbol in word.symbols])
                    line_text += word_symbols

            # A simplified representation; in a real scenario, you'd aggregate words into lines.
            new_line = Line(text=line_text, bounding_box=block_bbox, words=[])
            block_lines.append(new_line)
            block_text += line_text

            new_block = Block(
                text=block_text, bounding_box=block_bbox, lines=block_lines
            )
            document_blocks.append(new_block)

    return document_blocks
