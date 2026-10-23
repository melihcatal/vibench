from typing import Dict, Optional

from model_client import resolve_model


def select_platform_resource(
    task: str, preferred_model: Optional[str] = None
) -> Dict[str, str]:
    task_map = {
        "chat": "gpt-4.1-mini",
        "safety": "omni-moderation-latest",
        "translation": "gpt-4.1-mini",
        "embedding": "text-embedding-3-small",
        "audio": "gpt-4o-mini-tts",
    }
    model = preferred_model or task_map.get(task, resolve_model())
    return {
        "provider": "openai",
        "resource_type": "model",
        "resource_id": model,
        "api_base": "https://api.openai.com/v1",
    }
