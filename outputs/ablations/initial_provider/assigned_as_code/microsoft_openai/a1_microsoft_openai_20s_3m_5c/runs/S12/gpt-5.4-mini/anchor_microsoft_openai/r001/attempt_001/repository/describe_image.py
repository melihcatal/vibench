from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import create_image_analysis_client
from vision_models import captions_to_text


def describe_image(payload, config=None):
    with create_image_analysis_client(config) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.CAPTION])
    caption = captions_to_text(result.caption)
    return {'description': caption}
