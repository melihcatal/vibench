from google.cloud import vision

from vision_client import client, image_from_input
from vision_models import VisionAnalysisResult, VisionImageInput


def describe_image(image_path: str = None, image_bytes: bytes = None) -> VisionAnalysisResult:
    vision_client = client()
    image = image_from_input(VisionImageInput(image_path=image_path, image_bytes=image_bytes))
    response = vision_client.label_detection(image=image)
    description = " ".join(label.description for label in response.label_annotations[:5])
    return VisionAnalysisResult(provider="google-cloud-vision", kind="description", raw=vision.ImageAnnotatorClient.to_dict(response), description=description)
