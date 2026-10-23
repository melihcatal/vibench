import os
from typing import List

from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_azure_vision_client
from vision_models import normalize_labels, VisionLabels

def detect_image_labels(image_path: str) -&gt; VisionLabels:
    client = get_azure_vision_client()
    result = client.analyze(image_path, features=[VisualFeatures.TAGS])
    return normalize_labels(result)