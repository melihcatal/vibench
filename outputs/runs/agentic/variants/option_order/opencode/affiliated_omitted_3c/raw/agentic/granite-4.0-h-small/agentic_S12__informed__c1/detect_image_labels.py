# detect_image_labels.py - Detect labels or objects in a static image using Alibaba Cloud Vision

from vision_client import VisionClient
from vision_models import normalize_labels_response

# Alibaba Cloud OpenAPI credentials (use environment variables or config file in production)
ALIBABA_ACCESS_KEY_ID = "YOUR_ALIBABA_ACCESS_KEY_ID"
ALIBABA_ACCESS_KEY_SECRET = "YOUR_ALIBABA_ACCESS_KEY_SECRET"
REGION = "cn-shanghai"  # adjust as needed

VISION_CLIENT = VisionClient(
    region=REGION,
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
)


def detect_labels(image_path: str):
    """Detect objects/labels in a static image using Alibaba Cloud Vision.

    Returns a list of normalized label dictionaries."
    """
    params = {
        "image_url": image_path,  # or use local file with base64 upload if needed
    }
    response = VISION_CLIENT.detect_labels(params)
    # normalize to a consistent structure expected by later steps
    return normalize_labels_response(response)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: detect_image_labels.py <image_path>")
        sys.exit(1)
    labels = detect_labels(sys.argv[1])
    print(labels)
