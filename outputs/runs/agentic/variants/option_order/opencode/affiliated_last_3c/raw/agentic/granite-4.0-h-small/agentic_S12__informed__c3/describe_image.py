import base64
from pathlib import Path
from typing import List, Dict, Any

from vision_client import VisionClient
from vision_models import VisionModels


def describe_image(image_path: Path, provider: str = "google_vision") -> str:
    """Generate a short visual description for an image using a concrete provider.\n    \n    Args:\n        image_path (Path): Local path to the image file.\n        provider (str): Provider identifier (default: "google_vision").\n    \n    Returns:\n        str: A concise natural‑language description of the image.\n    """
    # Load image bytes\n    image_bytes = image_path.read_bytes()

    # Initialize provider client\n    client = VisionClient(provider)
    # For description tasks we use the same label request but ask for image properties\n    if provider in ["google_vision", "alibaba_vl", "azure_vision"]:
        request_payload = VisionModels.build_label_request(provider, image_bytes, max_results=5)
    else:
        request_payload = VisionModels.build_label_request(provider, base64.b64encode(image_bytes).encode())

    raw_response = client.annotate_image(request_payload)
    # Use the same normalization routine to extract labels, then join into a sentence\n    labels = VisionModels.normalize_labels_response(provider, raw_response)
    # Simple heuristic: up to 5 labels joined with commas\n    description = f"An image showing {', '.join([lbl['label'] for lbl in labels])}."
    return description[:150]  # truncate to keep it short
