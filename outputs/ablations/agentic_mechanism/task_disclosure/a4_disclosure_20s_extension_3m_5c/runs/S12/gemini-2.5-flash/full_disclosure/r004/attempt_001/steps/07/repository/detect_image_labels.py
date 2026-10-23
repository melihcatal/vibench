from google.cloud import vision

def detect_image_labels(image_path):
    """Detects labels in the image file."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = []
    for label in response.label_annotations:
        labels.append(label.description)
    return labels
