import requests


def metric_annotation_safety(text):
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": "${PERSPECTIVE_API_KEY}"}
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(endpoint, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
