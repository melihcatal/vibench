import boto3
import io
from PIL import Image
import pytesseract

def stored_document_ocr(bucket_name, object_key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    print(f'Extracted text: {text}')
    return text