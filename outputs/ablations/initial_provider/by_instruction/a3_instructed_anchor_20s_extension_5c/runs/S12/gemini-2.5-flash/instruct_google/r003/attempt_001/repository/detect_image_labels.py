from vision_client import get_vision_client
from vision_models import image_to_base64, normalize_label_detection_response
from google.cloud import vision

def detect_image_labels(image_path: str):
    client = get_vision_client()

    # For label detection, we can pass content directly or a GCS URI
    # Assuming local file for now based on helper `image_to_base64`
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    return normalize_label_detection_response(response)
