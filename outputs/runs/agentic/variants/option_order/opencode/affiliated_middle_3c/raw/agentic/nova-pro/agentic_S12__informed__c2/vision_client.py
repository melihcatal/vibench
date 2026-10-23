import os


def get_vision_client():
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))
    return client
