from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

def create_vision_client(endpoint, api_key):
    return ImageAnalysisClient(endpoint, AzureKeyCredential(api_key))