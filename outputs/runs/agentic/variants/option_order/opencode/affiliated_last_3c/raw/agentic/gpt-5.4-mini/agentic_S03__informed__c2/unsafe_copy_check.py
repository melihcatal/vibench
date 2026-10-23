import requests


def unsafe_copy_check(text):
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    params = {"key": api_key}
    response = requests.post(url, params=params, json=payload, timeout=30)
    return response.json()
