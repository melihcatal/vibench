from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def get_vision_client(endpoint, api_key):
    return ImageAnalysisClient(endpoint, AzureKeyCredential(api_key))