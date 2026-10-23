import requests


def payload_safety(text: str, api_key: str | None = None) -> dict:
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    resp = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        headers=headers,
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
    )
    data = resp.json()
    score = (
        data.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return {"provider": "perspective_api", "unsafe": score >= 0.5, "score": score}
