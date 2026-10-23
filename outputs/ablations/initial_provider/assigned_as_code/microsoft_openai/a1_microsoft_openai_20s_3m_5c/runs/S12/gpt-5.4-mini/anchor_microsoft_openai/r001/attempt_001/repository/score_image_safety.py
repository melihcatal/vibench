from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import create_image_analysis_client
from vision_models import safety_categories_to_risks


def score_image_safety(payload, config=None):
    with create_image_analysis_client(config) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.IMAGE_TYPE, VisualFeatures.OBJECTS])
    return {'safety': safety_categories_to_risks(getattr(result, 'categories', []))}
