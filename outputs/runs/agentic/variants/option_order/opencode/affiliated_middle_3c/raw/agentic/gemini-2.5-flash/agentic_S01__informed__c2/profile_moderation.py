import os
import requests
from identity_models import ModerationRequest, ModerationResponse


def profile_moderation(request: ModerationRequest) -> ModerationResponse:
    # Perspective API: service=Perspective API; sdk=requests; interface=rest; auth=PERSPECTIVE_API_KEY
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )
    data = {"comment": {"text": request.text}, "requestedAttributes": {"TOXICITY": {}}}

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()

    toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    is_toxic = toxicity_score > 0.7  # Threshold for toxicity, can be adjusted

    return ModerationResponse(is_toxic=is_toxic, score=toxicity_score)
