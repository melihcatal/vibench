import boto3
from vision_client import image_to_bytes
from vision_models import VisionSafety


def score_image_safety(image_path: str) -> VisionSafety:
    rekognition = boto3.client("rekognition")
    image_bytes = image_to_bytes(image_path)
    response = rekognition.detect_moderation_labels(Image={"Bytes": image_bytes})
    scores = {
        label["Name"]: label["Confidence"] for label in response["ModerationLabels"]
    }
    return VisionSafety(scores=scores)
