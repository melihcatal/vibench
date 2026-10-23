import google.cloud.vision


def check_script_safety(script):
    client = google.cloud.vision.ImageAnnotatorClient()
    image = google.cloud.vision.types.Image(content=script.encode('utf-8'))
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(response.error.message)
    return all(annotation.description.isalnum() for annotation in response.text_annotations)