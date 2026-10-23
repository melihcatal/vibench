import os
import boto3
from vision_client import load_image
from vision_models import parse_textract_text

def detect_image_text(image_path: str) -> str:
    content = load_image(image_path)
    textract = boto3.client('textract', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
    response = textract.detect_document_text(Document={'Bytes': content})
    return parse_textract_text(response)