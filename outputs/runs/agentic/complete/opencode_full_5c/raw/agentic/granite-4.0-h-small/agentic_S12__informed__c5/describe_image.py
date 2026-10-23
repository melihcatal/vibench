import json
from vision_client import VisionClient  # Amazon Rekognition


def describe_image(image_path: str) -> str:
    """Generates a concise visual description of an image using Amazon Rekognition.

    Returns a short text description.
    """
    client = VisionClient()  # Rekognition client via boto3
    response = client.describe_content(Image={"Bytes": client.read_image(image_path)})
    # Use title/description field if available, otherwise build from labels
    description = response.get("Description", "")
    if not description:
        labels = response.get("Labels", [])
        description = "Image contains " + ", ".join([lbl for lbl in labels])
    return description
