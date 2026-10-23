from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures


def detect_image_text(image_path):
    client = ImageAnalysisClient(
        endpoint=os.getenv("AZURE_VISION_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_VISION_KEY")),
    )
    result = client.analyze(image_path, visual_features=[VisualFeatures.TEXT])
    return result.text.value
