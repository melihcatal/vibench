import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from vision_client import get_azure_vision_client
from vision_models import ImageAnalysisRequest, ImageLabel


def detect_image_labels(request: ImageAnalysisRequest) -> List[ImageLabel]:
    client = get_azure_vision_client()

    if request.image_url:
        result = client.analyze(
            image_url=request.image_url, visual_features=[VisualFeatures.TAGS]
        )
    elif request.image_bytes:
        result = client.analyze(
            image_data=request.image_bytes, visual_features=[VisualFeatures.TAGS]
        )
    else:
        raise ValueError("Either image_url or image_bytes must be provided.")

    labels = []
    if result.tags:
        for tag in result.tags:
            labels.append(ImageLabel(name=tag.name, confidence=tag.confidence))
    return labels
