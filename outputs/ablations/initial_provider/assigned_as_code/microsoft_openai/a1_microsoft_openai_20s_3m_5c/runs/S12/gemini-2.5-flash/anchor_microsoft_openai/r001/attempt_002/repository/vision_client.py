from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


def get_image_analysis_client(endpoint: str, api_key: str):
    return ImageAnalysisClient(endpoint, AzureKeyCredential(api_key))
