from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures


def describe_image(image_path):
    client = ImageAnalysisClient(
        endpoint=os.getenv("AZURE_VISION_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_VISION_KEY")),
    )
    result = client.analyze(image_path, visual_features=[VisualFeatures.CAPTION])
    return result.caption.value
