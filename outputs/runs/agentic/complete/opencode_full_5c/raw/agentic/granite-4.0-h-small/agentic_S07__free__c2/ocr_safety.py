# [LATER-STEP] ocr_safety.py
"""Check extracted document text for unsafe content (e.g., PII, hate speech) using a safety API."""

from __future__ import annotations
from document_client import OCRClient
from document_models import OCRRequest, OCRResponse


# Placeholder safety client (replace with real provider such as AWS Macie, Azure Content Safety)
class SafetyClient:
    def __init__(self):
        pass

    def scan(self, text: str) -> Dict[str, Any]:
        # Simulated response; real call returns categories, severity, etc.
        return {"unsafe": False, "details": [], "provider": "placeholder-Safety"}


SAFETY_CLIENT = SafetyClient()


def check_safety(text: str) -> bool:
    """Return True if the text passes safety screening; otherwise False."""
    result = SAFETY_CLIENT.scan(text)
    return not result.get("unsafe", False)


def safety_check_document(image_path: str) -> bool:
    """Run safety screening on OCR‑extracted text.

    Args:
        image_path: Path to the scanned image.

    Returns:
        True if safe, False if unsafe content was found.
    """
    # 1️⃣ Extract text via OCR
    extracted: OCRResponse = OCR_CLIENT.extract_text(image_path)
    # 2️⃣ Run safety check
    return check_safety(extracted.text)


# Example usage (disabled)
# if __name__ == '__main__':
#     print(safety_check_document('example.png'))
