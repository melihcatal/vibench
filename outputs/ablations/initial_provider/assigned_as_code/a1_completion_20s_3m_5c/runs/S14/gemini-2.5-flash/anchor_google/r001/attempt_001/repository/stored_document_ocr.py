from google.cloud import vision
from google.cloud import storage
from storage_client import get_bucket_name, get_project_id

def stored_document_ocr(gcs_object_name: str):
    client = vision.ImageAnnotatorClient()

    image = vision.Image(
        source=vision.ImageSource(gcs_image_uri=f"gs://{get_bucket_name()}/{gcs_object_name}")
    )

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return {"extracted_text": texts[0].description}
    else:
        return {"extracted_text": ""}
