import requests
import os
from identity_models import ModerateProfileRequest, ModerateProfileResponse


def profile_moderation(request: ModerateProfileRequest) -> ModerateProfileResponse:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": request.profile_text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],  # Assuming English for this example
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        toxicity_score = (
            data.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value")
        )

        # Define a threshold for what is considered safe. This can be adjusted.
        # A lower score means less toxicity.
        is_safe = toxicity_score < 0.7 if toxicity_score is not None else True

        return ModerateProfileResponse(is_safe=is_safe, score=toxicity_score)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Perspective API moderation failed: {e}")
