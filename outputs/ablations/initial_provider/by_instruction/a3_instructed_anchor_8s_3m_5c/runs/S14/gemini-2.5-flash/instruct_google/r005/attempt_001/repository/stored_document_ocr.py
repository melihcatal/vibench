from google.cloud import vision
from storage_models import ObjectMetadataRequest

def run_ocr_on_stored_document(
    bucket_name: str, 
    object_name: str
) -> str:
    """Runs OCR on a stored document object in Google Cloud Storage using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    image = vision.Image({
        "source": {"image_uri": f"gs://{bucket_name}/{object_name}"}
    })

    response = client.document_text_detection(image=image)
    full_text = response.full_text_annotation.text
    
    return full_text
