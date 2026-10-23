from google.cloud import vision

def stored_document_ocr(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=blob.download_as_string())
    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation.text
    print('Texts: {}'.format(texts))