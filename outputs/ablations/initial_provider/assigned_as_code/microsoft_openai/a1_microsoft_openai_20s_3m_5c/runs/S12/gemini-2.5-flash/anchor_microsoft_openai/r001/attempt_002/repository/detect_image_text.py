from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def detect_image_text(payload, config=None):
    config = config or {}
    with ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.READ])
    text_content = ""
    for line in result.read.blocks[0].lines:
        text_content += line.text + "\n"
    return {'text_content': text_content.strip()}
