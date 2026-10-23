from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def score_image_safety(payload, config=None):
    config = config or {}
    with ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.ADULT])
    safety_score = result.adult.is_adult_content
    return {'safety_score': safety_score}