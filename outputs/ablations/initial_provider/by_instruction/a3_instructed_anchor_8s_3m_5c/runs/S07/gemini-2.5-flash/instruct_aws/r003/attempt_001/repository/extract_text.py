import base64
from typing import Dict, Any
from document_client import get_textract_client
from document_models import DocumentPage

def extract_text_from_image(image_bytes: bytes) -> Dict[int, DocumentPage]:
    textract_client = get_textract_client()
    response = textract_client.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    pages = {}
    blocks = response.get('Blocks', [])

    for block in blocks:
        if block['BlockType'] == 'PAGE':
            page_number = block['Page']
            page_text_blocks = [b for b in blocks if b.get('Page') == page_number and b['BlockType'] == 'LINE']
            page_text = "\n".join([b['Text'] for b in page_text_blocks if 'Text' in b])
            pages[page_number] = DocumentPage(
                page_number=page_number,
                text=page_text,
                blocks=[b for b in blocks if b.get('Page') == page_number]
            )
    return pages
