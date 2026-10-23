from vision_client import get_vision_client
from vision_models import VisionRequest, VisionResponse, normalize_response

def detect_labels(image_path):
    client = get_vision_client()
    image = VisionRequest(image_path)
    response = client.label_detection(image=image)
    normalized_response = normalize_response(response)
    return VisionResponse(normalized_response)