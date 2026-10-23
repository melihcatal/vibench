from google.cloud import vision

def get_vision_client():
    return vision.ImageAnnotatorClient()

def analyze_image(image_path):
    client = get_vision_client()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        return response.label_annotations