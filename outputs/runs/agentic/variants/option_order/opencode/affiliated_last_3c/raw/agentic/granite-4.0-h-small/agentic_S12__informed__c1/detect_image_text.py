import os
import dashscope
from vision_client import VisionClient
from vision_models import TextDetectionRequest, TextDetectionResponse

# Explicit provider identifier
PROVIDER = "DashScope"


def detect_image_text(image_path: str) -> TextDetectionResponse:
    """Extract OCR text from a static image using DashScope Qwen-VL.
    Returns a normalized TextDetectionResponse.
    """
    client = VisionClient()
    request = TextDetectionRequest(image_path=image_path)
    raw_response = client.text_detection(request)
    # Convert raw DashScope response to our normalized model
    return TextDetectionResponse.from_dashscope(raw_response)
