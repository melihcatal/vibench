from typing import Dict

import openai

from identity_client import build_identity_config


class ModerationError(RuntimeError):
    pass


def profile_moderation(profile_text: str) -> Dict[str, object]:
    cfg = build_identity_config()
    client = openai.OpenAI(api_key=cfg.api_key)
    result = client.moderations.create(model="omni-moderation-latest", input=profile_text)
    item = result.results[0]
    return {
        "flagged": item.flagged,
        "categories": dict(item.categories),
        "category_scores": dict(item.category_scores),
        "model": "omni-moderation-latest",
    }
