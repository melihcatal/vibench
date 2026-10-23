from vision_client import VisionClient
from vision_models import VisionImageInput


def detect_image_text(image_path: str):
    return VisionClient.from_env().detect_text(VisionImageInput(image_path=image_path))
