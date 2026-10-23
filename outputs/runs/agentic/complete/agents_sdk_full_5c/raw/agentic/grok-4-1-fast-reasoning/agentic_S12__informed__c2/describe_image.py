import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.core import BinaryData
from .vision_client import image_to_bytes
from .vision_models import Caption, VisionCaption

def describe_image(image_path: str) -> VisionCaption:
    endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    key = os.getenv('AZURE_VISION_KEY')
    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    image_data = BinaryData.from_bytes(image_to_bytes(image_path))
    poller = client.begin_analyze(image_input=image_data, visual_features=['Caption'])
    result = poller.result()
    caption_result = result.caption
    if caption_result and caption_result.text:
        caption = {
            'text': caption_result.text,
            'confidence': caption_result.confidence
        }
        return {'caption': caption}
    return {'caption': {'text': '', 'confidence': 0.0}}