from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def score_image_safety(payload, config=None):
    config = config or {}
    with ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.ADULT])
    adult_content = result.adult.is_adult_content
    racy_content = result.adult.is_racy_content
    safety_score = 0
    if not adult_content and not racy_content:
        safety_score = 100
    return {'safety_score': safety_score, 'is_safe': not adult_content and not racy_content}