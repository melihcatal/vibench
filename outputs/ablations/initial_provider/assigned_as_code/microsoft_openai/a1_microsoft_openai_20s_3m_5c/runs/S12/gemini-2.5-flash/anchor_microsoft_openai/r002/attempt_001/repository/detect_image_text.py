from azure.ai.vision.imageanalysis import VisualFeatures
from vision_client import get_image_analysis_client
from vision_models import normalize_text_response

def detect_image_text(payload, config=None):
    config = config or {}
    client = get_image_analysis_client()
    with client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.READ])
    return {'text_annotations': normalize_text_response(result)}
