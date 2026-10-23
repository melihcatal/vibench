import base64
from pathlib import Path
from typing import List, Dict, Any

from vision_client import VisionClient
from vision_models import VisionModels


def detect_image_text(
    image_path: Path, provider: str = "google_vision"
) -> List[Dict[str, str]]:
    """Detect text appearing inside a static image using a concrete provider.\n    \n    Args:\n        image_path (Path): Local path to the image file.\n        provider (str): Provider identifier (default: "google_vision").\n    \n    Returns:\n        List[Dict[str, str]]: List of detected text blocks with keys \"text\" and \"confidence\".\n"""
    # Load image bytes\n    image_bytes = image_path.read_bytes()

    # Initialize the provider client\n    client = VisionClient(provider)
    # Use the OCR request helper\n    request_payload = VisionModels.build_ocr_request(provider, image_bytes)

    # Invoke the provider\n    raw_response = client.annotate_image(request_payload)

    # Normalize the response to a uniform format\n    return VisionModels.normalize_ocr_response(provider, raw_response)
