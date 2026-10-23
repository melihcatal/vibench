import os
from perspectivetools import (
    PerspectiveApi,
)  # hypothetical client library for Perspective API
# Perspective API – identifies the concrete provider


def check_safety(ocr_text: str) -> dict:
    """Check extracted OCR text for unsafe content using the Perspective API.

    Args:
        ocr_text (str): Plain text from OCR.

    Returns:
        dict: JSON-like response containing toxicity scores.
    """
    # Initialize client using environment variable
    client = PerspectiveApi(os.getenv("PERSPECTIVE_API_KEY"))
    # Send the text for toxicity analysis
    response = client.analyze(toxicity=ocr_text)
    # Return the raw scores; structure may vary per library
    return response
