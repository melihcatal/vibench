import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from typing import Optional
from vision_client import get_azure_vision_client
from vision_models import ImageInput, ImageDescriptionResult

def describe_image(image_input: ImageInput) -> Optional[ImageDescriptionResult]:
    client = get_azure_vision_client()

    if image_input.image_bytes:
        image_data = image_input.image_bytes
    elif image_input.image_url:
        image_data = image_input.image_url
    else:
        raise ValueError("ImageInput must contain either image_bytes or image_url.")

    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.CAPTION],
        language="en",
        gender_neutral_caption=True
    )

    if result.caption and result.caption.text:
        return ImageDescriptionResult(
            caption=result.caption.text,
            confidence=result.caption.confidence
        )
    return None