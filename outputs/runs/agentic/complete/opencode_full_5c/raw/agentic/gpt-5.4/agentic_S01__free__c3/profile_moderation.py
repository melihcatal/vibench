from __future__ import annotations

from identity_client import openai_post
from identity_models import ModerationRequest


def profile_moderation(request: ModerationRequest):
    payload = {
        "model": "omni-moderation-latest",
        "input": request.profile_text,
    }
    response = openai_post(payload)
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "profile_text": request.profile_text,
        "moderation": response,
    }
