from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures


def score_image_safety(image_path):
    client = ImageAnalysisClient(
        endpoint=os.getenv("AZURE_VISION_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_VISION_KEY")),
    )
    result = client.analyze(image_path, visual_features=[VisualFeatures.ADULT])
    return result.adult.is_adult_content
