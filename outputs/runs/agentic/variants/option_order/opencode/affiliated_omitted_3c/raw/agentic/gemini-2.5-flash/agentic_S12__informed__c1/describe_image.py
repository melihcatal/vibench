import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from vision_client import get_azure_vision_client
from vision_models import ImageAnalysisRequest, ImageDescription


def describe_image(request: ImageAnalysisRequest) -> ImageDescription:
    client = get_azure_vision_client()

    if request.image_url:
        result = client.analyze(
            image_url=request.image_url, visual_features=[VisualFeatures.CAPTION]
        )
    elif request.image_bytes:
        result = client.analyze(
            image_data=request.image_bytes, visual_features=[VisualFeatures.CAPTION]
        )
    else:
        raise ValueError("Either image_url or image_bytes must be provided.")

    if result.caption:
        return ImageDescription(
            text=result.caption.text, confidence=result.caption.confidence
        )
    return ImageDescription(text="No description found.", confidence=0.0)
