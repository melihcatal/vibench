from model_client import get_platform_client
from typing import Dict, Any, Optional

def collect_platform_metadata(prompt: str, deployment: str = "gpt-4o-mini-deployment") -> Dict[str, Any]:
    client = get_platform_client()
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
    )
    usage = response.usage.dict() if response.usage else None
    return {
        "output": response.choices[0].message.content,
        "usage": usage,
        "model": response.model,
        "id": response.id,
        "created": response.created,
        "system_fingerprint": getattr(response, "system_fingerprint", None),
    }