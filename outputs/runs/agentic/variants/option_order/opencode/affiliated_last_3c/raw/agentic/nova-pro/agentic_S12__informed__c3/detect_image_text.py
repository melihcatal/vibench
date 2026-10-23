import google.cloud.vision as vision


def detect_image_text(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        image = vision.Image(content=image_file.read())
        response = client.text_detection(image=image)
        texts = [annotation.description for annotation in response.text_annotations]
        return texts
