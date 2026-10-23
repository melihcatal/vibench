import requests


def unsafe_copy_check(text: str) -> bool:
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return score >= 0.5
