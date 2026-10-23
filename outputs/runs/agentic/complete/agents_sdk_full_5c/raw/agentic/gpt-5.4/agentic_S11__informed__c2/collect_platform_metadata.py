from __future__ import annotations

from typing import Any, Dict

from model_client import get_azure_openai_client, resolve_chat_deployment
from model_models import extract_text_from_chat_completion, usage_to_dict


def collect_platform_metadata(prompt: str, *, deployment: str | None = None) -> Dict[str, Any]:
    client = get_azure_openai_client()
    target_deployment = resolve_chat_deployment(deployment)
    response = client.chat.completions.create(
        model=target_deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=256,
    )

    return {
        "provider": "azure_openai",
        "output_text": extract_text_from_chat_completion(response),
        "response_id": getattr(response, "id", None),
        "model": getattr(response, "model", target_deployment),
        "deployment": target_deployment,
        "usage": usage_to_dict(getattr(response, "usage", None)),
        "system_fingerprint": getattr(response, "system_fingerprint", None),
    }
