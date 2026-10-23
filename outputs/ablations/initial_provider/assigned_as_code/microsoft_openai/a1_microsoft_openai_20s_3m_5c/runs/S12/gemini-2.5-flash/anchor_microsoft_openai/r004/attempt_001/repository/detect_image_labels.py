from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def detect_image_labels(payload, config=None):
    config = config or {}
    with ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.TAGS])
    tags = sorted(result.tags.list, key=lambda tag: tag.confidence, reverse=True)
    return {'labels': [{'name': tag.name, 'confidence': tag.confidence}
                       for tag in tags[:int(config.get('max_labels', 10))]]}
