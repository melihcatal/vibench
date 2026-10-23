import requests
from vision_client import get_openai_vision_config, image_source_to_data_url
from vision_models import normalize_text_response


def detect_image_text(image_path: str):
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
                    {'type': 'text', 'text': 'Extract any readable text in the image. If none is visible, return an empty string.'},
                    {'type': 'image_url', 'image_url': {'url': data_url}},
                ]}
            ],
            'temperature': 0,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return normalize_text_response(resp.json())
