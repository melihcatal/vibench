import boto3
from document_client import get_textract_client
from document_models import ExtractedLayoutElement
from typing import List, Dict, Any

def extract_layout_elements(image_bytes: bytes) -> List[ExtractedLayoutElement]:
    """
    Extracts blocks, lines, tables, or layout elements from a document using AWS Textract.
    """
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        Features=['LAYOUT']
    )

    layout_elements: List[ExtractedLayoutElement] = []
    for block in response.get('Blocks', []):
        if block['BlockType'] in ['PAGE', 'LINE', 'WORD', 'TABLE', 'CELL', 'KEY_VALUE_SET', 'QUERY', 'QUERY_RESULT', 'TITLE', 'PARAGRAPH', 'LIST', 'FIGURE']:
            # For layout, we are interested in structural elements like TITLE, PARAGRAPH, LIST, FIGURE, TABLE
            # We can also include LINE and WORD if granular text layout is needed
            element_type = block['BlockType']
            text = block.get('Text')
            geometry = block.get('Geometry')
            confidence = block.get('Confidence')
            layout_elements.append(ExtractedLayoutElement(element_type, text, geometry, confidence))
            
    return layout_elements
