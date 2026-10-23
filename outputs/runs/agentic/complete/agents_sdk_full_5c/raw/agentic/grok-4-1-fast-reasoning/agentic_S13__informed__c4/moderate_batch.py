import requests
from safety_client import get_perspective_api_key
from safety_models import ModerationResult, BatchModerationResult

PERSPECTIVE_BATCH_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:batchAnalyze"

def moderate_batch(texts: list[str]) -> BatchModerationResult:
    api_key = get_perspective_api_key()
    requests_data = [
        {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {}
            }
        }
        for text in texts
    ]
    data = {"requests": requests_data}
    params = {"key": api_key}
    response = requests.post(PERSPECTIVE_BATCH_URL, json=data, params=params)
    response.raise_for_status()
    api_response = response.json()
    results = []
    for i, text in enumerate(texts):
        attr_scores = api_response["results"][i]["attributeScores"]
        scores = {
            attr: attr_scores[attr]["summaryScore"]["score"]["value"]
            for attr in attr_scores
        }
        flagged = any(score > 0.5 for score in scores.values())
        results.append(ModerationResult(
            input_text=text,
            flagged=flagged,
            categories={},
            scores=scores
        ))
    return BatchModerationResult(results=results)