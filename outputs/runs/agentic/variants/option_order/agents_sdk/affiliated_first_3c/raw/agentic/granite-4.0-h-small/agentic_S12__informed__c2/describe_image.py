# describe_image.py
from vision_client import VisionClient
from vision_models import ImageDescriptionResponse

def describe_image(image_path: str) -> ImageDescriptionResponse:
    client = VisionClient()
    # Azure AI Vision SDK example
    result = client.describe_image(image_path, max_number_of_descriptions=1, min_confidence=0.5)
    return ImageDescriptionResponse.from_sdk(result)
