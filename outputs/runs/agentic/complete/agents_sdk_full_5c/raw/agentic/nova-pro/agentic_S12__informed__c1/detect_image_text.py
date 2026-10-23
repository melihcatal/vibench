import os
from azure.ai.vision import ImageAnalysisClient, AzureKeyCredential

endpoint = os.getenv('AZURE_VISION_ENDPOINT')
key = os.getenv('AZURE_VISION_KEY')
client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))

def detect_text(image_path):
    with open(image_path, 'rb') as image_data:
        result = client.analyze(image_data, features=['text'])
    return result.text