import requests


def moderate_transcript(text: str):
    response = requests.post(
        "https://api.perspectiveapi.com/v1/comments:analyze",
        params={"key": __import__("os").getenv("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
