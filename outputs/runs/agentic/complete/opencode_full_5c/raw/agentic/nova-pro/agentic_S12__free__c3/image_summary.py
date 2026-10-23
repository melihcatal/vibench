import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

client = ImageAnalysisClient(
    endpoint=os.getenv("VISION_ENDPOINT"), credential=os.getenv("VISION_KEY")
)


def summarize_analysis(image_path):
    with open(image_path, "rb") as image_data:
        result = client.analyze(
            image_data, visual_features=[VisualFeatures.CAPTION, VisualFeatures.OBJECTS]
        )
        return f"Description: {result.caption.text}, Objects: {result.objects.value}"
