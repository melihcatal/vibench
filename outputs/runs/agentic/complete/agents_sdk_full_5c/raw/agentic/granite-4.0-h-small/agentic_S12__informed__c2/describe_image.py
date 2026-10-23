import os
import azure.ai.vision.imageanalysis as vision
from vision_client import VisionClient

def describe_image(image_path):
    client = VisionClient()
    analyser = client.create_image_analyser()
    result = analyser.describe_image(image_path)
    # Return a concise one‑sentence description
    return result.caption.text if result.caption else ""
