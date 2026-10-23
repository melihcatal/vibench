import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

client = ImageAnalysisClient(
    AZURE_VISION_ENDPOINT, AzureKeyCredential(AZURE_VISION_KEY)
)


def detect_labels(image_path):
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data=image_data, features=["objects"])
        return [label.name for label in result.objects.values]
