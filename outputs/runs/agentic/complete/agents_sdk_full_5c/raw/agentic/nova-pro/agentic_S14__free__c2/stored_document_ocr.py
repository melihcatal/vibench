import boto3
from google.cloud import vision

client = vision.ImageAnnotatorClient()

s3 = boto3.client('s3')

def stored_document_ocr(bucket_name, object_name):
    response = s3.get_object(Bucket=bucket_name, Key=object_name)
    image_content = response['Body'].read()
    image = vision.Image(content=image_content)
    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text