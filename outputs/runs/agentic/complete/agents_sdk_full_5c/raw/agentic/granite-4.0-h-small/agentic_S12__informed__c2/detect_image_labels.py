import os
import azure.ai.vision.imageanalysis as vision
from vision_client import VisionClient

def detect_image_labels(image_path):
    client = VisionClient()
    # Create an ImageAnalysisClient using environment configs (AZURE_VISION_ENDPOINT, AZURE_VISION_KEY)
    analyser = client.create_image_analyser()
    result = analyser.analyze_image_labels(image_path)
    # Return normalized list of label strings
    return [label.name for label in result.labels]
