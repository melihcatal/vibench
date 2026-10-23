import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient, ImageAnalysisFeature
from vision_client import image_to_bytes
from vision_models import ImageTexts

endpoint = os.getenv('AZURE_VISION_ENDPOINT')
key = os.getenv('AZURE_VISION_KEY')

def detect_image_text(image_path: str) -> ImageTexts:
    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = client.analyze(
        image=image_to_bytes(image_path),
        visual_features=[ImageAnalysisFeature.TEXT]
    )
    texts = []
    if result.text and result.text.lines:
        for line in result.text.lines:
            if line.text:
                texts.append(line.text)
    return {'texts': texts}