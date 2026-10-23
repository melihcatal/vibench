import io

from google.cloud import vision
from google.cloud import storage
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse

def run_ocr_on_stored_document(payload: StoredDocumentOcrRequest, config=None):
    config = config or {}
    # Initialize Google Cloud Vision client
    vision_client = vision.ImageAnnotatorClient()

    # Initialize Google Cloud Storage client to fetch the document
    storage_client = storage.Client(project=config["project_id"])
    bucket = storage_client.bucket(payload.bucket_name)
    blob = bucket.blob(payload.object_name)
    
    # Download the content of the object to memory
    image_content = blob.download_as_bytes()

    image = vision.Image(content=image_content)
    response = vision_client.document_text_detection(image=image)
    full_text = response.full_text_annotation.text

    return StoredDocumentOcrResponse(text_content=full_text)
