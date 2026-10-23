import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_claims(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(
        url, headers=headers, params={"key": PERSPECTIVE_API_KEY}, json=payload
    )
    analysis = response.json()
    toxicity_score = analysis["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    if toxicity_score > 0.5:
        return "Moderated"
    else:
        return "Approved"
