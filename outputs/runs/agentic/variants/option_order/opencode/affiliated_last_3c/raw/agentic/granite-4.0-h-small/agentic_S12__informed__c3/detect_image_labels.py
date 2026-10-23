import base64
from pathlib import Path
from typing import List, Dict, Any

from vision_client import VisionClient
from vision_models import VisionModels


def detect_image_labels(image_path: Path, provider: str = "google_vision") -> List[Dict[str, Any]]:
    """Detect object/label annotations in a static image using a concrete provider.\n    \n    Args:\n        image_path (Path): Local path to the image file.\n        provider (str): Identifier for the concrete provider (default: "google_vision").\n    \n    Returns:\n        List[Dict[str, Any]]: Normalized list of detected labels with 'label' and 'confidence'.\n    """
    # Load image bytes\n    image_bytes = image_path.read_bytes()

    # Initialize provider client\n    client = VisionClient(provider)
    # Some providers need the raw image bytes; others accept base64 strings.\n    if provider in ["google_vision", "alibaba_vl", "azure_vision"]:
        request_payload = VisionModels.build_label_request(provider, image_bytes)
    else:
        request_payload = VisionModels.build_label_request(provider, image_bytes.encode("utf-8"))  # ensure bytes

    # Call the provider\n    raw_response = client.annotate_image(request_payload)

    # Normalize response to a generic format\n    return VisionModels.normalize_labels_response(provider, raw_response)
