import boto3
from vision_client import get_aws_rekognition_client
from vision_models import ImageSafetyReport, SafetyLabel

def check_image_for_unsafe_content(image_bytes: bytes, min_confidence: float = 75.0) -> ImageSafetyReport:
    """
    Checks an image for unsafe content using AWS Rekognition Content Moderation.

    Args:
        image_bytes: The byte content of the image.
        min_confidence: The minimum confidence level for moderation labels.

    Returns:
        An ImageSafetyReport object.
    """
    rekognition_client: boto3.client = get_aws_rekognition_client()
    response = rekognition_client.detect_moderation_labels(
        Image={"Bytes": image_bytes},
        MinConfidence=min_confidence,
    )

    safety_labels = []
    if "ModerationLabels" in response and response["ModerationLabels"]:
        for label_data in response["ModerationLabels"]:
            safety_labels.append(
                SafetyLabel(
                    name=label_data["Name"],
                    confidence=label_data["Confidence"],
                )
            )

    is_safe = not bool(safety_labels)
    return ImageSafetyReport(safe=is_safe, labels=safety_labels)
