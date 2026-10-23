import requests

from identity_client import perspective_api_key, request_timeout
from identity_models import ProfileModerationRequest, normalize_perspective_response


def profile_moderation(request: ProfileModerationRequest):
    response = requests.post(
        f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key()}",
        json={
            "comment": {"text": request.profile_text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {},
            },
            "languages": [request.locale] if request.locale else ["en"],
        },
        timeout=request_timeout(),
    )
    response.raise_for_status()
    moderated = normalize_perspective_response(response.json())
    moderated["user_id"] = request.user_id
    return moderated
