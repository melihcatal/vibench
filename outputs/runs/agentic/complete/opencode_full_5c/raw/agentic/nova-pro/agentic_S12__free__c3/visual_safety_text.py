import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

client = ImageAnalysisClient(
    endpoint=os.getenv("VISION_ENDPOINT"), credential=os.getenv("VISION_KEY")
)


def check_safety_text(text):
    with open("sample_image.jpg", "rb") as image_data:
        result = client.analyze(image_data, visual_features=[VisualFeatures.TEXT])
        return text not in result.text.value
