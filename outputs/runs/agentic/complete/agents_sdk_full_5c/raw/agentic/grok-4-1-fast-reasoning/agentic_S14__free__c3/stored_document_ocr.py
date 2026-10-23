import io
from storage_client import get_s3_client
from google.cloud import vision

def ocr_stored_document(bucket: str, key: str) -> str:
    """
    Performs OCR using Google Cloud Vision on a stored document object in S3.
    Supports images and single-page PDFs.
    """
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()
    
    client = vision.ImageAnnoterClient()
    image = vision.Image(content=image_content)
    
    result = client.text_detection(image=image)
    texts = result.text_annotations
    
    return texts[0].description if texts else ''