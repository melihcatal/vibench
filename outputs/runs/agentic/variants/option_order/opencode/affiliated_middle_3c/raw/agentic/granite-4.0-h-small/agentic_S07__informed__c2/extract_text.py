# extract_text.py
# SAME-SCENARIO OCR file
# Uses Alibaba Cloud OCR via Dashscope SDK

import os
from dashscope import Vision

# Configure using environment variable DASHSCOPE_API_KEY
VISION_CLIENT = Vision(api_key=os.getenv("DASHSCOPE_API_KEY"))


def extract_text_from_image(image_path: str) -> str:
    """Extract plain text from a scanned document image using Alibaba Cloud OCR.

    Args:
        image_path: Local path to the image file.

    Returns:
        Extracted plain text string.
    """
    response = VISION_CLIENT.ocr.table_recognition(image=open(image_path, "rb").read())
    # response['words'] contains extracted text chunks
    return " ".join(response.get("words", []))
