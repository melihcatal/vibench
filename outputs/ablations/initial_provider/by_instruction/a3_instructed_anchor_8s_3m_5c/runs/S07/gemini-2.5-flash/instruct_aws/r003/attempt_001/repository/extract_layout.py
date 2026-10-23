import base64
from typing import Dict, Any, List
from document_client import get_textract_client
from document_models import DocumentLayout

def extract_layout_from_image(image_bytes: bytes) -> Dict[int, DocumentLayout]:
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['LAYOUT']
    )

    pages = {}
    blocks = response.get('Blocks', [])

    for block in blocks:
        if block['BlockType'] == 'PAGE':
            page_number = block['Page']
            page_blocks = [b for b in blocks if b.get('Page') == page_number]
            pages[page_number] = DocumentLayout(
                page_number=page_number,
                blocks=page_blocks
            )
    return pages
