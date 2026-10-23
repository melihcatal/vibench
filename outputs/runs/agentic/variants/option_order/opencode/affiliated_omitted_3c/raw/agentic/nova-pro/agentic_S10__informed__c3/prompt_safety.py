import requests

PERSPECTIVE_API_KEY = "your-perspective-api-key"


def check_prompt_safety(text: str) -> bool:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json={"comment": {"text": text}, "languages": ["en"]},
        params={"key": PERSPECTIVE_API_KEY},
    )
    return response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] < 0.5
