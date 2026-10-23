from google.cloud import vision

def detect_document_text_from_gcs(gcs_uri: str) -> str:
    """Detects document text in the image located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = gcs_uri

    response = client.document_text_detection(image=image)
    return response.full_text

