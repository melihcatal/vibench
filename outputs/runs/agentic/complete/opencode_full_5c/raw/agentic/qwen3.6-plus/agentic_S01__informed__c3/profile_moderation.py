import os
import requests
from identity_models import ModerationRequest, ModerationResponse


PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_profile_text(
    text: str,
    attributes: list = None,
    threshold: float = 0.7,
) -> ModerationResponse:
    if attributes is None:
        attributes = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "PROFANITY"]

    request = ModerationRequest(text=text, attributes=attributes)
    payload = request.to_perspective_payload(api_key=PERSPECTIVE_API_KEY)

    params = {"key": PERSPECTIVE_API_KEY}
    resp = requests.post(PERSPECTIVE_API_URL, json=payload, params=params)
    resp.raise_for_status()
    data = resp.json()

    return ModerationResponse.from_perspective_response(data, threshold=threshold)


if __name__ == "__main__":
    result = moderate_profile_text(
        text="This is a friendly profile bio.",
    )
    print(result)
