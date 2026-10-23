import os
from vision_client import AzureVisionClient
from vision_models import ImageAnalysisRequest, ImageDescription
from azure.ai.vision.imageanalysis import VisualFeatures


def describe_image(request: ImageAnalysisRequest) -> ImageDescription | None:
    client = AzureVisionClient().get_client()

    result = client.analyze(
        image_data=request.image_data, visual_features=[VisualFeatures.CAPTION]
    )

    if result.caption is not None:
        return ImageDescription(
            text=result.caption.text, confidence=result.caption.confidence
        )
    return None
