from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def describe_image(payload, config=None):
    config = config or {}
    with ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.CAPTION])
    caption = result.caption.text if result.caption else "No description found."
    return {'description': caption, 'confidence': result.caption.confidence if result.caption else 0.0}
