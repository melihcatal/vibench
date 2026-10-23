from google.cloud import vision

def ocr_request(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.document_text_detection(image=image)
    return response

def layout_request(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.text_detection(image=image)
    return response

def normalize_response(response):
    if response.error.message:
        raise Exception(response.error.message)
    return response