import requests


def metric_annotation_safety(annotation_text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "comment": {"text": annotation_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "spanAnnotations": False,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
