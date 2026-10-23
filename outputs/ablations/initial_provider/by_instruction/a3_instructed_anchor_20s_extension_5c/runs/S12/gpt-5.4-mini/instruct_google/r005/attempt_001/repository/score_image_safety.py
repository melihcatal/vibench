from google.cloud import vision

from vision_client import build_image, get_google_vision_client, safe_search_from_response


def score_image_safety(image_path: str):
    client = get_google_vision_client()
    response = client.safe_search_detection(image=build_image(image_path))
    return safe_search_from_response(response)
