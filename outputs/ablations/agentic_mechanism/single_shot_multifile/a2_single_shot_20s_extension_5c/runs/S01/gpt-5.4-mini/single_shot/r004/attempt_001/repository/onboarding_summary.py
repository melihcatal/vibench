from typing import Any, Dict

import requests

from identity_client import get_identity_settings, json_headers, user_agent_headers

_PROVIDER_HOST = "https://api.openai.com"
_PROVIDER_MODEL = "gpt-4.1-mini"


def onboarding_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    settings = get_identity_settings()
    url = f"{_PROVIDER_HOST}/v1/chat/completions"
    headers = user_agent_headers({**json_headers(), "Authorization": f"Bearer {settings.api_key}"})
    payload = {"model": _PROVIDER_MODEL, "messages": [{"role": "user", "content": str(state)}], "temperature": 0.2}
    response = requests.post(url, json=payload, headers=headers, timeout=settings.timeout_seconds)
    response.raise_for_status()
    data = response.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return {"summary": content, "model": _PROVIDER_MODEL}
