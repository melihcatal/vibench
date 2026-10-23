from vision_client import VisionClient
from vision_models import ImageInput, RekognitionModerationLabel


def score_image_safety(image_input: ImageInput) -> list[RekognitionModerationLabel]:
    rekognition_client = VisionClient().get_rekognition_client()
    response = rekognition_client.detect_moderation_labels(
        Image=image_input.to_rekognition_input()
    )
    return [
        RekognitionModerationLabel(label)
        for label in response.get("ModerationLabels", [])
    ]
