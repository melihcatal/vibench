import os
from vision_client import AzureVisionClient
from vision_models import ImageAnalysisRequest, ImageLabel
from azure.ai.vision.imageanalysis import VisualFeatures


def detect_image_labels(request: ImageAnalysisRequest) -> list[ImageLabel]:
    client = AzureVisionClient().get_client()

    # Authenticate and construct client
    # Set the visual features you want to enable.
    # In this example, we will enable TAGS and CAPTION.
    result = client.analyze(
        image_data=request.image_data, visual_features=[VisualFeatures.TAGS]
    )

    labels = []
    if result.tags_result is not None:
        for tag in result.tags_result.values:
            labels.append(ImageLabel(name=tag.name, confidence=tag.confidence))
    return labels
