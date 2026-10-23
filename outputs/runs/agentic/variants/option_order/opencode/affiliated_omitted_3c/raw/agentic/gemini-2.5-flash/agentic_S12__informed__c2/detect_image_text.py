import os
from vision_client import AzureVisionClient
from vision_models import ImageAnalysisRequest, ImageText
from azure.ai.vision.imageanalysis import VisualFeatures


def detect_image_text(request: ImageAnalysisRequest) -> list[ImageText]:
    client = AzureVisionClient().get_client()

    result = client.analyze(
        image_data=request.image_data, visual_features=[VisualFeatures.READ]
    )

    texts = []
    if result.read_result is not None:
        for line in result.read_result.lines:
            # The bounding box is a list of 8 numbers representing x, y coordinates of 4 points.
            # We'll just pass it as is for now.
            texts.append(ImageText(text=line.text, bounding_box=line.bounding_box))
    return texts
