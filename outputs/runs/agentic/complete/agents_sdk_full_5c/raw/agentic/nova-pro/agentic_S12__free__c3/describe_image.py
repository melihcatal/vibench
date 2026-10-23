from google.cloud import vision

def describe_image(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        labels = response.label_annotations
        return ' '.join([label.description for label in labels])
