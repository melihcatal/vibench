from google.cloud import vision

def run_ocr_on_document(bucket_name: str, file_name: str) -> str:
    """
    Runs OCR on a document stored in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        file_name: The name of the file in the bucket.

    Returns:
        The extracted text from the document.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = f"gs://{bucket_name}/{file_name}"

    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text
