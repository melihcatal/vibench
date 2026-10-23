import requests
from vision_client import get_openai_vision_config
from vision_models import normalize_text_response


def alt_text_translate(description, target_language):
    cfg = get_openai_vision_config()
    resp = requests.post(
        f"{cfg.api_base}/chat/completions",
        headers={
            'Authorization': f'Bearer {cfg.api_key}',
            'Content-Type': 'application/json',
        },
        json={
            'model': cfg.model,
            'messages': [
                {'role': 'user', 'content': f'Translate this image description into {target_language}: {description}'}
            ],
            'temperature': 0,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return normalize_text_response(resp.json())
