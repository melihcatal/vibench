from vision_client import VisionClient
from vision_models import VisionImageInput


def detect_image_labels(image_path: str):
    return VisionClient.from_env().detect_labels(VisionImageInput(image_path=image_path))
