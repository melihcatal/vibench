import requests

PERSPECTIVE_API_KEY = "your-perspective-api-key"


def moderate_text(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "spanAnnotations": False,
    }
    response = requests.post(
        url, headers=headers, json=data, params={"key": PERSPECTIVE_API_KEY}
    )
    response.raise_for_status()
    return response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] < 0.5
