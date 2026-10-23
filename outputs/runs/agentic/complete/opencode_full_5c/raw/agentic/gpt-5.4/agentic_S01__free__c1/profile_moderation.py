from identity_client import openai_request
from identity_models import ModerationRequest, normalize_openai_moderation


def profile_moderation(profile_text: str) -> dict:
    request = ModerationRequest(profile_text=profile_text)
    payload = {
        "model": "omni-moderation-latest",
        "input": request.profile_text,
    }
    response = openai_request("/v1/moderations", payload)
    return normalize_openai_moderation(response)
