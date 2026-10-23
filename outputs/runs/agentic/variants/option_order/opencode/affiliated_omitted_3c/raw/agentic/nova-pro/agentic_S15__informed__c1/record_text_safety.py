import requests


def check_safety(text):
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/commentanalyzer/analyze",
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        headers={
            "Content-Type": "application/json",
            "API-Key": os.getenv("PERSPECTIVE_API_KEY"),
        },
    )
    return response.json()
