from google.cloud import vision

from vision_client import build_image, get_google_vision_client, text_from_response


def detect_image_text(image_path: str) -> str:
    client = get_google_vision_client()
    response = client.text_detection(image=build_image(image_path))
    return text_from_response(response)
