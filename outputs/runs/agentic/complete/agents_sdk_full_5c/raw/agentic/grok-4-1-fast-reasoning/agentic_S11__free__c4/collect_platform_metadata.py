from model_client import get_platform_client
from model_models import normalize_request
from typing import Dict, Any

def collect_platform_metadata(
    prompt: str,
    deployment: str,
    temperature: float = 0.7
) -> Dict[str, Any]:
    client = get_platform_client()
    messages = [{"role": "user", "content": prompt}]
    request = normalize_request(deployment, messages, temperature=temperature)
    response = client.chat.completions.create(**request)
    return {
        "content": response.choices[0].message.content,
        "model": response.model,
        "id": response.id,
        "created": response.created,
        "usage": response.usage.model_dump() if response.usage else None,
        "system_fingerprint": getattr(response, "system_fingerprint", None),
    }
