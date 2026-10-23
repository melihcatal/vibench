import requests

PERSPECTIVE_API_KEY = "your_api_key"


def platform_output_safety(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
