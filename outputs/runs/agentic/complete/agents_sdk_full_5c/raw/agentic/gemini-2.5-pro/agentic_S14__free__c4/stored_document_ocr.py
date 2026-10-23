from google.cloud import vision
from storage_client import get_storage_client, get_bucket_name
from storage_models import OcrResult

def run_ocr_on_stored_document(object_name: str, bucket_name: str = None) -> OcrResult:
    """
    Downloads a document from S3 and performs OCR using Google Cloud Vision API.

    :param object_name: The key of the document object in the S3 bucket.
    :param bucket_name: The S3 bucket. Defaults to env config.
    :return: An OcrResult object containing the extracted text.
    """
    s3_client = get_storage_client()
    target_bucket = bucket_name or get_bucket_name()

    # 1. Download document from S3
    try:
        s3_object = s3_client.get_object(Bucket=target_bucket, Key=object_name)
        content = s3_object["Body"].read()
    except Exception as e:
        print(f"Failed to download {object_name} from S3: {e}")
        raise

    # 2. Call Google Cloud Vision API for OCR
    vision_client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    response = vision_client.document_text_detection(image=image)
    
    if response.error.message:
        raise Exception(
            f"Google Cloud Vision API error: {response.error.message}"
        )
    
    full_text = response.full_text_annotation.text
    detected_language = "und" # Default undetermined
    if response.full_text_annotation.pages:
        page = response.full_text_annotation.pages[0]
        if page.property.detected_languages:
            detected_language = page.property.detected_languages[0].language_code

    return OcrResult(
        key=object_name,
        text=full_text,
        language=detected_language
    )
