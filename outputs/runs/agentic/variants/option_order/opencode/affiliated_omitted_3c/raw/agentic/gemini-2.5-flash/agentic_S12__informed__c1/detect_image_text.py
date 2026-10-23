import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from vision_client import get_azure_vision_client
from vision_models import ImageAnalysisRequest, ImageTextLine, ImageTextResult


def detect_image_text(request: ImageAnalysisRequest) -> ImageTextResult:
    client = get_azure_vision_client()

    if request.image_url:
        result = client.analyze(
            image_url=request.image_url, visual_features=[VisualFeatures.TEXT]
        )
    elif request.image_bytes:
        result = client.analyze(
            image_data=request.image_bytes, visual_features=[VisualFeatures.TEXT]
        )
    else:
        raise ValueError("Either image_url or image_bytes must be provided.")

    lines = []
    if result.text:
        for line in result.text.lines:
            lines.append(
                ImageTextLine(text=line.text, bounding_box=line.bounding_polygon)
            )
    return ImageTextResult(lines=lines)
