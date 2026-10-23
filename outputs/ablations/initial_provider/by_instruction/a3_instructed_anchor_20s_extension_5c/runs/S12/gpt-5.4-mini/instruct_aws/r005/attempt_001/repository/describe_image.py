from typing import Dict

from vision_client import VisionClient
from vision_models import ImageAnalysisRequest


def describe_image(image_path: str) -> Dict[str, str]:
    client = VisionClient()
    request = ImageAnalysisRequest(image_path=image_path)
    summary = client.describe_image(request)
    return {"provider": "aws.rekognition", "description": summary}
