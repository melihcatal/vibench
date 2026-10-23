
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

AZURE_VISION_ENDPOINT = os.environ.get("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.environ.get("AZURE_VISION_KEY")

def describe_image(image_url: str) -> str:
    """Generates a short visual description for an image using Azure AI Vision."""
    if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
        raise ValueError("Azure Vision endpoint and key must be set in environment variables.")

    client = ImageAnalysisClient(
        endpoint=AZURE_VISION_ENDPOINT,
        credential=AzureKeyCredential(AZURE_VISION_KEY)
    )

    result = client.analyze(image_url=image_url, visual_features=[VisualFeatures.CAPTION])

    if result.caption and result.caption.text:
        return result.caption.text
    return "No description generated."

if __name__ == '__main__':
    # Set AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables.
    # Example image URL:
    # test_image_url = "https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png"
    test_image_url = os.environ.get("TEST_IMAGE_URL_AZURE", "https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png")
    print(f"Describing image: {test_image_url}")
    description = describe_image(test_image_url)
    print(f"Description: {description}")
