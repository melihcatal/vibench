# detect_image_text.py - Detect text appearing inside an image using Alibaba Cloud OCR

from vision_client import VisionClient
from vision_models import normalize_text_detection_response

# Alibaba Cloud credentials (use env vars in production)
ALIBABA_ACCESS_KEY_ID = "YOUR_ALIBABA_ACCESS_KEY_ID"
ALIBABA_ACCESS_KEY_SECRET = "YOUR_ALIBABA_ACCESS_KEY_SECRET"
REGION = "cn-shanghai"

CLIENT = VisionClient(
    region=REGION,
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
)


def detect_text(image_path: str):
    """Extract text from an image via Alibaba Cloud OCR service.

    Returns a list of dictionaries with 'text' and 'region' keys.
    """
    resp = CLIENT.ocr_text(image_path=image_path)
    return normalize_text_detection_response(resp)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: detect_image_text.py <image_path>")
        sys.exit(1)
    texts = detect_text(sys.argv[1])
    for t in texts:
        (print(f"Region: {t['region']}, Text: {t['text']}"),)
