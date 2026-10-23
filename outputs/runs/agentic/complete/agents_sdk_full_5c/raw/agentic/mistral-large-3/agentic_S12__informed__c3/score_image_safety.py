from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from vision_client import get_image_bytes
from vision_models import ImageSafetyResponse
import os

def score_image_safety(image_path: str) -> ImageSafetyResponse:
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    image_bytes = get_image_bytes(image_path)
    
    result = client.analyze(
        image_data=image_bytes,
        visual_features=[VisualFeatures.SMART_CROPS, VisualFeatures.RACY_CONTENT, VisualFeatures.ADULT_CONTENT]
    )
    
    safety_scores = {
        "adult_score": result.adult.adult_score,
        "racy_score": result.adult.racy_score,
        "is_safe": result.adult.adult_score < 0.5 and result.adult.racy_score < 0.5
    }
    return ImageSafetyResponse(
        provider="azure_ai_vision",
        safety_scores=safety_scores,
        raw_response=result
    )