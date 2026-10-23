import base64
from google.cloud import vision_v1
from vision_client import get_google_vision_client
from vision_models import prepare_image_for_google, parse_google_vision_text_detection

def detect_image_text(image_bytes: bytes):
    client = get_google_vision_client()
    image = vision_v1.Image(content=prepare_image_for_google(image_bytes)['content'])
    response = client.text_detection(image=image)
    return parse_google_vision_text_detection(response)
