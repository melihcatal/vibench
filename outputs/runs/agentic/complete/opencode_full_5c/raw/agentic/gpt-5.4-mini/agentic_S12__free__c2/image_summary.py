import requests
from vision_client import get_openai_vision_config
from vision_models import normalize_text_response


def image_summary(labels, description, text):
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
                {'role': 'user', 'content': f'Summarize these visual analysis results briefly: labels={labels}; description={description}; text={text}'}
            ],
            'temperature': 0.2,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return normalize_text_response(resp.json())
