import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_claims(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": PERSPECTIVE_API_KEY}
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, params=params, json=payload)
    return response.json()
