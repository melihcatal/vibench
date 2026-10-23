import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import ImageAnalysisOptions, VisualFeatures

# Initialize the client
endpoint = os.getenv('VISION_ENDPOINT')
key = os.getenv('VISION_KEY')
client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))

def get_client():
    return client