from vision_client import get_clarifai_moderation_model
from vision_models import ImageSafetyReport

def score_image_safety(image_path: str) -> ImageSafetyReport:
    model = get_clarifai_moderation_model()
    response = model.predict_by_filename(filename=image_path)
    concepts = response['outputs'][0]['data']['concepts'][:10]
    high_risk = [concept['name'] for concept in concepts if concept['value'] > 0.8]
    return {
        'is_safe': len(high_risk) == 0,
        'risks': high_risk
    }