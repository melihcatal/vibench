# score_image_safety.py - Check an image for unsafe or policy-sensitive visual content using Amazon Rekognition

from vision_client import VisionClient
from vision_models import normalize_safety_score

# AWS credentials (use env vars or config in production)
AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
REGION = "us-east-1"

CLIENT = VisionClient(
    region=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def safe_analysis(image_path: str):
    """
    Run safety/content moderation on an image via Amazon Rekognition.

    Returns a dict with 'unsafe' boolean and 'categories' list of detected unsafe categories.
    """
    resp = CLIENT.detect_moderation(image_path=image_path)
    return normalize_safety_score(resp)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: score_image_safety.py <image_path>")
        sys.exit(1)
    result = safe_analysis(sys.argv[1])
    print(result)
