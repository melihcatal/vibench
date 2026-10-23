from google.cloud import vision

def stored_document_ocr(bucket_name, blob_name):
    client = vision.ImageAnnotatorClient()
    storage_client = storage.Client()
    blob = storage_client.bucket(bucket_name).blob(blob_name)
    content = blob.download_as_bytes()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation.text
    print(f"Texts: {texts}")
    return texts
