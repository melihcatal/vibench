# detect_image_text.py
from vision_client import VisionClient
from vision_models import ImageTextDetectionResponse

def detect_image_text(image_path: str) -> ImageTextDetectionResponse:
    client = VisionClient()
    # Azure AI Vision SDK example
    result = client.read_text(image_path, mode='Printed')
    return ImageTextDetectionResponse.from_sdk(result)
