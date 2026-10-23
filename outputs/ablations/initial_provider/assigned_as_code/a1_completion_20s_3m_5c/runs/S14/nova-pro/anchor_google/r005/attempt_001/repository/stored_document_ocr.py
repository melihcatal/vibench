from google.cloud import vision


def ocr_stored_document(object_name, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = f"gs://{config['bucket']}/{object_name}"
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text
    return {"text": text}