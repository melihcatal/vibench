from google.cloud import vision

from vision_client import get_vision_client, make_image


def describe_image(image_path=None, image_uri=None):
    client = get_vision_client()
    image = make_image(image_path=image_path, image_uri=image_uri)
    response = client.label_detection(image=image, max_results=5)
    labels = [item.description for item in response.label_annotations[:3]]
    return ", ".join(labels)
