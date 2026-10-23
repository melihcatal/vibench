import os
import azure.ai.vision.imageanalysis as vision
from vision_client import VisionClient

def detect_image_text(image_path):
    client = VisionClient()
    analyser = client.create_image_analyser()
    result = analyser.read_text(image_path)
    # Return all detected text lines
    return result.read_results[0].lines
