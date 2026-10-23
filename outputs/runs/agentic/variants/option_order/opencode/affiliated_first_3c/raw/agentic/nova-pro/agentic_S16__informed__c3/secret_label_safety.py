import requests


def check_secret_labels_safety(secret_labels):
    url = "https://api.perspectiveapi.com/v1alpha1/commentAnalyzer"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer PERSPECTIVE_API_KEY",
    }
    data = {"comment": {"text": secret_labels}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
