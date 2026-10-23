from dashscope import MultiModalConversation
from vision_models import normalize_safety


def score_image_safety(image_path: str):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    resp = MultiModalConversation.call(
        model='qwen-vl-max',
        messages=[{'role': 'user', 'content': [{'image': image_bytes}, {'text': 'Assess whether this image contains unsafe or policy-sensitive visual content and return a safety judgment.'}]}],
    )
    return normalize_safety(getattr(resp, 'output', resp))
