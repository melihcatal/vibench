from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures


def detect_image_labels(image_path):
    client = ImageAnalysisClient(
        endpoint=os.getenv("AZURE_VISION_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_VISION_KEY")),
    )
    result = client.analyze(image_path, visual_features=[VisualFeatures.OBJECTS])
    return result.objects.value
