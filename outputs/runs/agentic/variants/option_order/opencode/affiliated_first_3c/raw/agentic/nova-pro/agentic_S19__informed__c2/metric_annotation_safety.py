import requests


def check_metric_annotation_safety(text):
    response = requests.post(
        "https://api.perspectiveapi.com/v1/commentAnalysis",
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        headers={"Authorization": f"Bearer {PERSPECTIVE_API_KEY}"},
    )
    return response.json()
