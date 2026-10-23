import boto3
from PIL import Image
import io

from storage_client import get_s3_client


def ocr_stored_document(object_name):
    client = get_s3_client()
    response = client.get_object(Bucket='your-bucket-name', Key=object_name)
    image = Image.open(io.BytesIO(response['Body'].read()))
    # Perform OCR on the image
    # This is a placeholder for actual OCR implementation
    return 'Extracted text from OCR'