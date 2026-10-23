from azure.ai.vision.imageanalysis import VisualFeatures
from vision_client import get_image_analysis_client

def score_image_safety(payload, config=None):
    config = config or {}
    client = get_image_analysis_client()
    with client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.CATEOGRIES])
    
    safety_scores = {
        'adult_score': result.categories.adult.score if result.categories and result.categories.adult else 0.0,
        'gore_score': result.categories.gory.score if result.categories and result.categories.gory else 0.0,
        'self_harm_score': result.categories.self_harm.score if result.categories and result.categories.self_harm else 0.0,
        'sexual_score': result.categories.sexual.score if result.categories and result.categories.sexual else 0.0,
        'violence_score': result.categories.violence.score if result.categories and result.categories.violence else 0.0
    }
    
    return {'safety_scores': safety_scores}
