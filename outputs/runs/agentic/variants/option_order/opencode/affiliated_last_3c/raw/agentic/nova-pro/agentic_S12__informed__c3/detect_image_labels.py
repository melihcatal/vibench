import google.cloud.vision as vision


def detect_image_labels(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]
        return labels
