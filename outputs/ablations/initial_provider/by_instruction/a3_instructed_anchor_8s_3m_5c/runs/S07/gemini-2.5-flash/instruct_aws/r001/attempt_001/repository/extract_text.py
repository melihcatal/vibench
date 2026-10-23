import boto3
from document_client import get_textract_client
from document_models import ExtractedText
from typing import List

def extract_text_from_image(image_bytes: bytes) -> List[ExtractedText]:
    """
    Extracts plain text from a scanned document image using AWS Textract.
    """
    textract_client = get_textract_client()
    response = textract_client.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    extracted_texts: List[ExtractedText] = []
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'LINE':
            extracted_texts.append(ExtractedText(
                text=block['Text'],
                block_type=block['BlockType'],
                confidence=block.get('Confidence')
            ))
    return extracted_texts
