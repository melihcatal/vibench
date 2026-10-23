import os
from dashscope import MultiModalConversation
from vision_models import normalize_labels


def detect_image_labels(image_path: str):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    resp = MultiModalConversation.call(
        model='qwen-vl-max',
        messages=[{'role': 'user', 'content': [{'image': image_bytes}, {'text': 'List the main labels and objects in this image.'}]}],
    )
    return normalize_labels(getattr(resp, 'output', resp))
