from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import create_image_analysis_client
from vision_models import read_text_lines


def detect_image_text(payload, config=None):
    with create_image_analysis_client(config) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.READ])
    return {'text': read_text_lines(result.read)}
