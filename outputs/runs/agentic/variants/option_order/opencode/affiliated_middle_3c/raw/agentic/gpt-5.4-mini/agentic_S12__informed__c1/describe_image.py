from dashscope import MultiModalConversation
from vision_models import normalize_text


def describe_image(image_path: str):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    resp = MultiModalConversation.call(
        model='qwen-vl-max',
        messages=[{'role': 'user', 'content': [{'image': image_bytes}, {'text': 'Describe this image in one short sentence.'}]}],
    )
    return normalize_text(getattr(resp, 'output', resp))
