import google.cloud.vision as vision


def describe_image(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        description = " ".join(
            [label.description for label in response.label_annotations]
        )
        return description
