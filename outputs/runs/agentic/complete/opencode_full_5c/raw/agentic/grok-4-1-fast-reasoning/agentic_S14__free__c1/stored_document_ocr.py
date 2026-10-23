import io
from google.cloud import vision
from storage_client import get_storage_client


def ocr_stored_document(bucket: str, object_key: str) -> str:
    s3_client = get_storage_client()
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    image_content = response["Body"].read()
    vision_client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    result = vision_client.text_detection(image=image)
    texts = result.text_annotations
    return texts[0].description if texts else ""
