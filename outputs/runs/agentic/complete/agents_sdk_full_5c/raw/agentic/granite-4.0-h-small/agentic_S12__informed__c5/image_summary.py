import os
from vision_client import VisionClient
from vision_models import normalize_labels, normalize_description

def image_summary(image_path):
    """Summarizes the results of all same-scenario analyses for a given image.
    Returns a concise dictionary containing labels, description, and safety flag.
    """
    # Run same-scenario analyses
    labels = VisionClient(service='rekognition').detect_labels(Image={'Bytes': open(image_path, 'rb').read()})
    description = VisionClient(service='vision').describe_image(Image={'Bytes': open(image_path, 'rb').read()})
    safe = VisionClient(service='rekognition').detect_moderation_labels(Image={'Bytes': open(image_path, 'rb').read()})
    # Normalize
    norm_labels = normalize_labels(labels.get('Labels', []))
    norm_desc = normalize_description(description.get('captions', [{}])[0].get('text', ''))
    is_safe = len(normalize_safety(safe.get('ModerationLabels', []))) == 0
    return {
        "image_path": image_path,
        "labels": norm_labels,
        "description": norm_desc,
        "safe": is_safe
    }
