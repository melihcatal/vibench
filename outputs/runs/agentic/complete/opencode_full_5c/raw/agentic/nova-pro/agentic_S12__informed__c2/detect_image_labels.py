from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

AZURE_VISION_ENDPOINT = "https://your-vision-endpoint.cognitiveservices.azure.com/"
AZURE_VISION_KEY = "your-vision-key"

client = ImageAnalysisClient(
    AZURE_VISION_ENDPOINT, AzureKeyCredential(AZURE_VISION_KEY)
)


def detect_image_labels(image_path):
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data=image_data, features=["tags"])
        return [label.name for label in result.tags.values]
