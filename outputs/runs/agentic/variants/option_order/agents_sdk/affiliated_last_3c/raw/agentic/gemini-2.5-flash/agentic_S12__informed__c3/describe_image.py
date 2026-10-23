import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def describe_image(image_url: str):
    """Generates a short visual description for an image using Azure AI Vision."""
    endpoint = os.environ["AZURE_VISION_ENDPOINT"]
    key = os.environ["AZURE_VISION_KEY"]

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    result = client.analyze(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION]
    )

    if result.caption:
        return result.caption.text
    return None

if __name__ == '__main__':
    # This example requires AZURE_VISION_ENDPOINT and AZURE_VISION_KEY to be set.
    # For demonstration:
    # print(describe_image("https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png"))
    pass
