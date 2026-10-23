import os

from google.cloud import vision

from storage_client import get_bucket_name, get_object_key, get_s3_client


def stored_document_ocr(bucket=None, key=None):
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=get_bucket_name(bucket), Key=get_object_key(key))
    data = obj["Body"].read()
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=data)
    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text if response.full_text_annotation else ""
