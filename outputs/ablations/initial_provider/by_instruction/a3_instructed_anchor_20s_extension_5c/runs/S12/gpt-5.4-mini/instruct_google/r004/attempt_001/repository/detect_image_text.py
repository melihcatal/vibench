from google.cloud import vision

from vision_client import client, image_from_input
from vision_models import VisionAnalysisResult, VisionImageInput, normalize_text


def detect_image_text(image_path: str = None, image_bytes: bytes = None) -> VisionAnalysisResult:
    vision_client = client()
    image = image_from_input(VisionImageInput(image_path=image_path, image_bytes=image_bytes))
    response = vision_client.text_detection(image=image)
    text = normalize_text([{"text": annotation.description, "score": 0.0} for annotation in response.text_annotations])
    return VisionAnalysisResult(provider="google-cloud-vision", kind="text", raw=vision.ImageAnnotatorClient.to_dict(response), text=text)
