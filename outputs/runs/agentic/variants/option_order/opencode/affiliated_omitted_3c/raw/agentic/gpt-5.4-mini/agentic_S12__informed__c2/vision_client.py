import os
from typing import Any, Dict

import boto3

from vision_models import ImageAnalysisRequest, ImageAnalysisResult, normalize_labels, normalize_safety, normalize_text


PROVIDER_NAME = 'amazon-rekognition'


def load_config() -> Dict[str, Any]:
    return {
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
        'aws_profile': os.getenv('AWS_PROFILE'),
    }


def client():
    cfg = load_config()
    session = boto3.session.Session(profile_name=cfg['aws_profile'], region_name=cfg['aws_region'])
    return session.client('rekognition')


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()


def analyze_labels(request: ImageAnalysisRequest):
    response = client().detect_labels(Image={'Bytes': load_image_bytes(request.image_path)}, MaxLabels=request.max_results)
    return ImageAnalysisResult(labels=normalize_labels(response.get('Labels')), raw=response)


def analyze_text(request: ImageAnalysisRequest):
    response = client().detect_text(Image={'Bytes': load_image_bytes(request.image_path)})
    return ImageAnalysisResult(text=normalize_text(response.get('TextDetections')), raw=response)


def analyze_safety(request: ImageAnalysisRequest):
    response = client().detect_moderation_labels(Image={'Bytes': load_image_bytes(request.image_path)})
    return ImageAnalysisResult(safety=normalize_safety(response.get('ModerationLabels')), raw=response)
