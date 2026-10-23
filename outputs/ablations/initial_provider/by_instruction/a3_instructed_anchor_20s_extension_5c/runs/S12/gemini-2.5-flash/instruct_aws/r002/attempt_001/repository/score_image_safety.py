from vision_client import get_rekognition_client
import os

class ScoreImageSafetyRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes

class SafetyLabel:
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence

class ScoreImageSafetyResponse:
    def __init__(self, safety_labels: list[SafetyLabel]):
        self.safety_labels = safety_labels

def score_image_safety(request: ScoreImageSafetyRequest) -> ScoreImageSafetyResponse:
    rekognition_client = get_rekognition_client()
    response = rekognition_client.detect_moderation_labels(
        Image={'Bytes': request.image_bytes}
    )
    safety_labels = [
        SafetyLabel(name=label['Name'], confidence=label['Confidence'])
        for label in response['ModerationLabels']
    ]
    return ScoreImageSafetyResponse(safety_labels=safety_labels)
