from google.cloud import vision

from storage_client import get_storage_client, get_vision_client
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse

def run_ocr_on_stored_document(
    request: StoredDocumentOcrRequest
) -> StoredDocumentOcrResponse:
    """Runs OCR on a stored document object in Google Cloud Storage using Google Cloud Vision API."""
    vision_client = get_vision_client()

    # Specify the GCS URI of the image
    gcs_source_uri = f"gs://{request.bucket_name}/{request.object_name}"
    source = vision.ImageSource(gcs_image_uri=gcs_source_uri)
    image = vision.Image(source=source)

    # Perform document text detection
    response = vision_client.document_text_detection(image=image)
    full_text = response.full_text_annotation.text
    
    text_annotations = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    text_annotations.append({
                        "text": word_text,
                        "bounds": [{"x": v.x, "y": v.y} for v in word.bounding_box.vertices],
                    })

    return StoredDocumentOcrResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        full_text=full_text,
        text_annotations=text_annotations,
    )
