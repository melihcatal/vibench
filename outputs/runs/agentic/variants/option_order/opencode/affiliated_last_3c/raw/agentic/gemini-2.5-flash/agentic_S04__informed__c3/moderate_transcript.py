import requests
from speech_client import speech_client
from speech_models import ModerationRequest

TOXICITY_THRESHOLD = 0.7  # Example threshold


def moderate_transcript(request: ModerationRequest) -> dict:
    if not speech_client.perspective_api_key:
        return {"error": "PERSPECTIVE_API_KEY not set"}

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + speech_client.perspective_api_key
    )
    data = {
        "comment": {"text": request.text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(url, json=data)
    response.raise_for_status()

    analysis_result = response.json()
    toxicity_score = analysis_result["attributeScores"]["TOXICITY"]["summaryScore"][
        "value"
    ]

    is_toxic = toxicity_score > TOXICITY_THRESHOLD

    return {
        "text": request.text,
        "toxicity_score": toxicity_score,
        "is_toxic": is_toxic,
    }
