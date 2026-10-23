from google.cloud import vision

from vision_client import build_image, get_google_vision_client, labels_from_response


def detect_image_labels(image_path: str):
    client = get_google_vision_client()
    response = client.label_detection(image=build_image(image_path))
    return labels_from_response(response)
