import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Initialize the client
endpoint = os.getenv("AZURE_VISION_ENDPOINT")
key = os.getenv("AZURE_VISION_KEY")
client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))


def detect_image_labels(image_path):
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data)
        return result.labels
