from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def detect_image_text(payload, config=None):
    config = config or {}
    with ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.READ])
    text_content = []
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                text_content.append(line.text)
    return {'text_content': text_content}
