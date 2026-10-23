import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


def load_vision_config(config=None):
    merged = dict(config or {})
    merged.setdefault('endpoint', os.environ.get('AZURE_VISION_ENDPOINT'))
    merged.setdefault('api_key', os.environ.get('AZURE_VISION_API_KEY'))
    merged.setdefault('max_labels', 10)
    merged.setdefault('max_text_items', 20)
    merged.setdefault('max_safety_items', 20)
    return merged


def open_image_client(config=None):
    cfg = load_vision_config(config)
    return ImageAnalysisClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key']))
