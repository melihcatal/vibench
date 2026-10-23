import requests


def visual_safety_text(text: str):
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").getenv("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=60,
    )
    response.raise_for_status()
    return {"provider": "perspective-api", "raw": response.json()}
