from document_client import get_document_vision_client
from google.cloud import vision

class ExtractedLayout:
    def __init__(self, pages: list):
        self.pages = pages

def extract_layout_elements(image_content: bytes) -> ExtractedLayout:
    client = get_document_vision_client()
    image = vision.Image(content=image_content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    pages_data = []
    for page in document.pages:
        blocks_data = []
        for block in page.blocks:
            paragraphs_data = []
            for paragraph in block.paragraphs:
                words_data = []
                for word in paragraph.words:
                    symbol_texts = [symbol.text for symbol in word.symbols]
                    words_data.append("".join(symbol_texts))
                paragraphs_data.append(" ".join(words_data))
            blocks_data.append("\n".join(paragraphs_data))
        pages_data.append({"blocks": blocks_data})

    return ExtractedLayout(pages_data)
