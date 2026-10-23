import os
import requests
from translation_models import UnsafeCopyCheckRequest, UnsafeCopyCheckResponse


def unsafe_copy_check(request: UnsafeCopyCheckRequest) -> UnsafeCopyCheckResponse:
    """
    Checks for unsafe content using the Google Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {
        "comment": {"text": request.text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }

    response = requests.post(url, json=data)
    response.raise_for_status()

    results = response.json()
    scores = {
        attr: results["attributeScores"][attr]["summaryScore"]["value"]
        for attr in results["attributeScores"]
    }

    return UnsafeCopyCheckResponse(scores=scores)
