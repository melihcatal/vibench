from google.cloud import vision


def moderate_vendor_text(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text.encode('utf-8'))
    if response.error.message:
        raise Exception(response.error.message)
    texts = response.text_annotations
    for text in texts:
        if 'vendor' in text.description.lower():
            return text.description
    return None