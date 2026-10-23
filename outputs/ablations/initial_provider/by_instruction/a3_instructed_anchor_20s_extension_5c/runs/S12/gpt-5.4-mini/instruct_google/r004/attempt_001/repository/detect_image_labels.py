from google.cloud import vision

from vision_client import client, image_from_input
from vision_models import VisionAnalysisResult, VisionImageInput, normalize_labels


def detect_image_labels(image_path: str = None, image_bytes: bytes = None) -> VisionAnalysisResult:
    vision_client = client()
    image = image_from_input(VisionImageInput(image_path=image_path, image_bytes=image_bytes))
    response = vision_client.label_detection(image=image)
    labels = normalize_labels([{"name": label.description, "score": label.score} for label in response.label_annotations])
    return VisionAnalysisResult(provider="google-cloud-vision", kind="labels", raw=vision.ImageAnnotatorClient.to_dict(response), labels=labels)
