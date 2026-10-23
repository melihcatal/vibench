import os

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


def load_vision_config(config=None):
    merged = dict(config or {})
    merged.setdefault('endpoint', os.environ.get('AZURE_VISION_ENDPOINT', ''))
    merged.setdefault('api_key', os.environ.get('AZURE_VISION_KEY', ''))
    merged.setdefault('max_labels', int(os.environ.get('AZURE_VISION_MAX_LABELS', '10')))
    merged.setdefault('language', os.environ.get('AZURE_VISION_LANGUAGE', 'en'))
    return merged


def build_client(config):
    return ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key']))
