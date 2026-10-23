import requests
from vision_client import get_openai_vision_config, image_source_to_data_url
from vision_models import normalize_text_response


def describe_image(image_path: str):
    cfg = get_openai_vision_config()
    data_url = image_source_to_data_url(image_path)
    resp = requests.post(
        f"{cfg.api_base}/chat/completions",
        headers={
            'Authorization': f'Bearer {cfg.api_key}',
            'Content-Type': 'application/json',
        },
        json={
            'model': cfg.model,
            'messages': [
                {'role': 'user', 'content': [
                    {'type': 'text', 'text': 'Write a short, natural visual description of this image in one sentence.'},
                    {'type': 'image_url', 'image_url': {'url': data_url}},
                ]}
            ],
            'temperature': 0.2,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return normalize_text_response(resp.json())
