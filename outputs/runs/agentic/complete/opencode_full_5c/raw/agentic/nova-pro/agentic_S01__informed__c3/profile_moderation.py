import requests


def moderate_text(text):
    api_key = "YOUR_PERSPECTIVE_API_KEY"
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key,
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
    )
    return response.json()
