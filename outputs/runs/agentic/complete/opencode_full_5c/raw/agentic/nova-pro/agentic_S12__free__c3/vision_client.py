import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient


def get_client():
    return ImageAnalysisClient(
        endpoint=os.getenv("VISION_ENDPOINT"), credential=os.getenv("VISION_KEY")
    )
