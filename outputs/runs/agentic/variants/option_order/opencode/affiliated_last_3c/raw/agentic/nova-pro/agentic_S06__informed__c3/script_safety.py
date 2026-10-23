import requests


def check_safety(script):
    perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + perspective_api_key
    )
    payload = {
        "comment": {"text": script},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=payload)
    return response.json()
