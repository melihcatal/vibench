import os
import azure.ai.vision.imageanalysis as vision
from vision_client import VisionClient

def score_image_safety(image_path):
    client = VisionClient()
    analyser = client.create_image_analyser()
    result = analyser.analyze_safety(image_path)
    # Return a safety score (0.0 = unsafe, 1.0 = safe)
    return result.safety_score
