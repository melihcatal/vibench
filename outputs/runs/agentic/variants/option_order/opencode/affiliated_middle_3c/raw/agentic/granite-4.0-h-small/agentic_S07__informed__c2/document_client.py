# document_client.py
# LOCAL HELPER file
# Provides unified configuration and client initialization for OCR and layout extraction steps

import os
from typing import Any, Dict

# ----- OCR CLIENT INITIALIZATION -----
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise RuntimeError(
        "Set DASHSCOPE_API_KEY environment variable for Alibaba Cloud OCR"
    )

from dashscope import Vision

VISION_CLIENT = Vision(api_key=DASHSCOPE_API_KEY)

# ----- LAYOUT CLIENT INITIALIZATION -----
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS for Google Document AI")

from google.cloud import documentai_v1 as documentai

LAYOUT_CLIENT = documentai.DocumentProcessorServiceClient()

# ----- COMMON UTILITIES -----


def load_config(config_path: str) -> Dict[str, Any]:
    """Load JSON/YAML config used across services.
    Placeholder - replace with actual loader if needed.
    """
    import json

    with open(config_path, "r") as f:
        return json.load(f)


def normalize_image_bytes(image_path: str) -> bytes:
    """Read image file and return raw bytes suitable for OCR APIs."""
    with open(image_path, "rb") as f:
        return f.read()
