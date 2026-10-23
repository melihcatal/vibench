import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def describe_image(image_data: bytes) -> str:
    endpoint = os.environ["AZURE_VISION_ENDPOINT"]
    key = os.environ["AZURE_VISION_KEY"]

    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.CAPTION],
        gender_neutral_captions=True,
    )

    if result.caption and result.caption.text:
        return result.caption.text
    return "No description found."
