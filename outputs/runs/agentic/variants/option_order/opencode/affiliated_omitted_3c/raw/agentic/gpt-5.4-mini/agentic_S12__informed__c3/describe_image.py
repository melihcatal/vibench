from vision_client import VisionClient
from vision_models import VisionImageInput


def describe_image(image_path: str):
    return VisionClient.from_env().describe_image(VisionImageInput(image_path=image_path))
