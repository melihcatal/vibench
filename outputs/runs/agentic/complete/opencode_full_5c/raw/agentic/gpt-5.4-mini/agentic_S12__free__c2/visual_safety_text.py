import requests
from vision_client import get_openai_vision_config
from vision_models import normalize_safety_response


def visual_safety_text(labels):
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
                {'role': 'user', 'content': f'Check these visual labels for unsafe text or policy-sensitive terms and return a safety verdict: {labels}'}
            ],
            'temperature': 0,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return normalize_safety_response(resp.json())
