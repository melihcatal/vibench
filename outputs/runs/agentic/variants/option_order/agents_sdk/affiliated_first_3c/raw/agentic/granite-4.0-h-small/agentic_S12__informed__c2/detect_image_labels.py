# detect_image_labels.py
from vision_client import VisionClient
from vision_models import ImageLabelsResponse

def detect_image_labels(image_path: str) -> ImageLabelsResponse:
    client = VisionClient()
    # Azure AI Vision SDK example
    result = client.analyze_image_labels(image_path)
    # Normalize result to our local model
    return ImageLabelsResponse.from_sdk(result)
