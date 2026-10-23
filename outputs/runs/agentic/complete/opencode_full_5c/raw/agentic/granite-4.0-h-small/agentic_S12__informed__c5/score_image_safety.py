import json
from vision_client import VisionClient  # Amazon Rekognition


def score_image_safety(image_path: str) -> bool:
    """Checks an image for unsafe or policy-sensitive visual content using Amazon Rekognition.

    Returns True if the image is considered safe, otherwise False.
    """
    client = VisionClient()  # Rekognition client via boto3
    response = client.detect_inappropriate_content(
        Image={"Bytes": client.read_image(image_path)}
    )
    # Assume response includes a SafeLabel flag (pseudo‑code, adapt to actual SDK)
    return response.get("IsSafe", True)
