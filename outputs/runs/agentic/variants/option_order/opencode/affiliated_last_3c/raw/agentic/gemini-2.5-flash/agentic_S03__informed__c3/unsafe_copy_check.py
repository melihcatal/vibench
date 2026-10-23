import requests
from translation_client import get_tisane_api_key
from translation_models import ContentSafetyRequest


def check_unsafe_content(request: ContentSafetyRequest) -> dict:
    api_key = get_tisane_api_key()
    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable not set.")

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,  # Provider-identifying signal
    }
    payload = {
        "language": request.language,
        "content": request.text,
        "settings": {
            "withSub": True,
            "document": {"explain": False, "quality": True, "user": {"id": "user123"}},
        },
    }

    # Tisane API endpoint
    url = "https://api.tisane.ai/parse"  # Provider API hostname

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
