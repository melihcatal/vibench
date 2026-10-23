import boto3
import pytesseract
from PIL import Image

def ocr_image(bucket_name, object_key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image = Image.open(response['Body'])
    text = pytesseract.image_to_string(image)
    return text