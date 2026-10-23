import requests

PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def log_text_safety(text: str, threshold: float = 0.5) -> dict:
    params = {"key": __import__("os").environ.get("PERSPECTIVE_API_KEY", "")}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_API_ENDPOINT, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"unsafe": score >= threshold, "score": score, "provider": "Perspective API"}
