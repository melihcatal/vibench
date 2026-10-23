from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


def get_vision_client():
    AZURE_VISION_ENDPOINT = "https://your-vision-endpoint.cognitiveservices.azure.com/"
    AZURE_VISION_KEY = "your-vision-key"
    client = ImageAnalysisClient(
        AZURE_VISION_ENDPOINT, AzureKeyCredential(AZURE_VISION_KEY)
    )
    return client
