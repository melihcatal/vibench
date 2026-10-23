import requests


def visual_safety_text(text):
    url = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    params = {"key": "${PERSPECTIVE_API_KEY}"}
    response = requests.post(url, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
