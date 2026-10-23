from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

def get_vision_client():
    endpoint = "https://api.cognitive.microsoft.com/vision/v3.1/"
    key = os.getenv('VISION_API_KEY')
    client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))
    return client

def normalize_response(response):
    # Placeholder for response normalization logic
    return response