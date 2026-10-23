from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def score_image_safety(payload, config=None):
    config = config or {}
    with ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.analyze(image_data=payload['image_bytes'],
                                visual_features=[VisualFeatures.ADULT, VisualFeatures.VIOLENCE])
    safety_scores = {
        'adult': {
            'is_adult_content': result.adult.is_adult_content,
            'is_racy_content': result.adult.is_racy_content,
            'is_gory_content': result.adult.is_gory_content,
            'adult_score': result.adult.adult_score,
            'racy_score': result.adult.racy_score,
            'gory_score': result.adult.gory_score,
        },
        'violence': {
            'has_violence': result.violence.has_violence,
            'violence_score': result.violence.violence_score,
        }
    }
    return safety_scores
