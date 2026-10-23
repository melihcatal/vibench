# detect_image_text.py
# [SAME-SCENARIO]

from vision_client import VisionClient
from vision_models import OcrResponse, extract_ocr_text

# Use Azure Computer Vision as the concrete provider
# Azure Computer Vision extracts printed and handwritten text from images


def detect_text(image_path: str) -> OcrResponse:
    """Detect and extract text appearing in an image using Azure Computer Vision.

    Returns an OcrResponse with the detected text lines and words.
    """
    client = VisionClient()  # Azure Vision client configured internally
    raw_resp = client.read(image_path)
    return extract_ocr_text(raw_resp)
