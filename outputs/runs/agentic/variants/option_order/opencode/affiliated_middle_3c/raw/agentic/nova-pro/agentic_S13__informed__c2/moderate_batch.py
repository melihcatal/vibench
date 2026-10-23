import requests


def moderate_batch(messages):
    api_key = "PERSPECTIVE_API_KEY"
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    results = []
    for message in messages:
        data = {
            "comment": {"text": message},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"],
        }
        response = requests.post(url, json=data, headers=headers)
        results.append(response.json())
    return results
