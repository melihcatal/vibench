from google.cloud import vision

def get_vision_client():
    return vision.ImageAnnotatorClient()

def get_image(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    return vision.Image(content=content)