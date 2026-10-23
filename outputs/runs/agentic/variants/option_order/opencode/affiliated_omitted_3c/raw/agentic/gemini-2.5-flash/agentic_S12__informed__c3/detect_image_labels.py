from vision_client import VisionClient
from vision_models import ImageInput, RekognitionLabel


def detect_image_labels(image_input: ImageInput) -> list[RekognitionLabel]:
    rekognition_client = VisionClient().get_rekognition_client()
    response = rekognition_client.detect_labels(
        Image=image_input.to_rekognition_input(), MaxLabels=10, MinConfidence=70
    )
    return [RekognitionLabel(label) for label in response.get("Labels", [])]
