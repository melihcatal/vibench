from google.cloud import vision

def get_client():
    return vision.ImageAnnotatorClient()

def get_image(image_path):
    with open(image_path, 'rb') as image_file:
        return vision.Image(content=image_file.read())

def get_response(client, image):
    return client.document_text_detection(image=image)