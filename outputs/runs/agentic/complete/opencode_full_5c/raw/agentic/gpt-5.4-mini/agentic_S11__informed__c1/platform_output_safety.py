import requests


def platform_output_safety(text: str) -> bool:
    url = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(
        url, params={"key": "${PERSPECTIVE_API_KEY}"}, json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return score < 0.5
