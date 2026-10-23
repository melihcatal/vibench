import os
from azure.core.credentials import AzureKeyCredential


def get_vision_client():
    return ImageAnalysisClient(
        endpoint=os.getenv("AZURE_VISION_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_VISION_KEY")),
    )
