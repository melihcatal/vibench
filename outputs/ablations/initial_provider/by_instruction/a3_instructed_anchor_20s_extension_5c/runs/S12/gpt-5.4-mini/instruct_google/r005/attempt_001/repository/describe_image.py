from google.cloud import vision

from vision_client import build_image, get_google_vision_client, labels_from_response


def describe_image(image_path: str) -> str:
    client = get_google_vision_client()
    response = client.label_detection(image=build_image(image_path))
    labels = labels_from_response(response)
    return ", ".join(labels[:3])
