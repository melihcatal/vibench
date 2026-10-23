from google.cloud import vision

def describe_image(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        description = response.label_annotations[0].description if response.label_annotations else ''
        return description