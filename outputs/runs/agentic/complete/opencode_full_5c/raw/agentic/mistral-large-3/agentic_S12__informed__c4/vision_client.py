from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import os
from typing import Optional


def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initializes and returns a Google Cloud Vision client."""
    return vision_v1.ImageAnnotatorClient()
