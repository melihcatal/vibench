from google.cloud import vision

def ocr_document(bucket_name, object_name):
    """Performs OCR on a stored document object."""
    client = vision.ImageAnnotatorClient()
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    content = blob.download_as_bytes()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text