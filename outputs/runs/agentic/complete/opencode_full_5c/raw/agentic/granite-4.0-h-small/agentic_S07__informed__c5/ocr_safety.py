# [LATER-STEP] ocr_safety.py

import os
from document_client import DocumentClient, load_env_vars
from document_models import OcrResult, normalize_ocr_response

# Safety provider env vars (choose Azure Content Safety as example)
REQUIRED_SAFETY_VARS = ["AZURE_CONTENT_SAFETY_ENDPOINT", "AZURE_CONTENT_SAFETY_KEY"]


def check_safety_of_text(text: str) -> dict:
    """Run safety/content moderation on extracted OCR text.

    Uses Azure AI Content Safety to detect unsafe content categories.
    Returns a dictionary of detected labels and corresponding scores.
    """
    load_env_vars(REQUIRED_SAFETY_VARS)
    client = DocumentClient(service="azure_ai_content_safety")
    result = client.detect_safety(text=text)
    return {"labels": result.get("labels", []), "scores": result.get("scores", {})}


def check_image_safety(image_path: str) -> dict:
    """Extract text then run safety check on the extracted content.

    Args:
        image_path: Local path to scanned image.

    Returns:
        Safety result dict.
    """
    client = DocumentClient(service="mindee")
    raw_ocr = client.ocr(image_path=image_path)
    norm = normalize_ocr_response(provider="mindee", raw_response=raw_ocr)
    extracted = norm.text
    return check_safety_of_text(extracted)


def main():
    image_file = "sample_document.jpg"
    safety = check_image_safety(image_file)
    print("Safety Check Result:")
    print(safety)


if __name__ == "__main__":
    main()
