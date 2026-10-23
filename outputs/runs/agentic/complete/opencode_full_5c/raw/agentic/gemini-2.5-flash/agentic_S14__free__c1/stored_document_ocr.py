from google.cloud import vision
from storage_client import get_storage_client
from storage_models import OcrRequest


def stored_document_ocr(request: OcrRequest):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(
        {"source": {"image_uri": f"gs://{request.bucket_name}/{request.object_name}"}}
    )
    response = client.document_text_detection(image=image)
    return {"full_text": response.full_text_annotation.text}
