import os

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_models import normalized_config


def load_vision_config(config=None):
    merged = normalized_config(config)
    merged.setdefault('endpoint', os.environ.get('AZURE_VISION_ENDPOINT'))
    merged.setdefault('api_key', os.environ.get('AZURE_VISION_API_KEY'))
    return merged


def create_image_analysis_client(config=None):
    cfg = load_vision_config(config)
    return ImageAnalysisClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key']))


def default_visual_features():
    return [VisualFeatures.TAGS, VisualFeatures.CAPTION, VisualFeatures.READ, VisualFeatures.SMART_CROPS, VisualFeatures.OBJECTS]
