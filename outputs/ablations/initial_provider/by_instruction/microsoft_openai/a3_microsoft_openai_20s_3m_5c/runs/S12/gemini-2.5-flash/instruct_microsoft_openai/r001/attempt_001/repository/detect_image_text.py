from vision_client import VisionClient
from vision_models import normalize_text_detection_response
from google.cloud import vision

def detect_image_text(image_url: str) -> list[str]:
    client_helper = VisionClient()
    gcv_client = client_helper.get_gcv_client()

    try:
        image = vision.Image()
        image.source.image_uri = image_url

        response = gcv_client.text_detection(image=image)
        return normalize_text_detection_response(response.model_dump())
    except Exception as e:
        print(f"Error detecting image text: {e}")
        return []
