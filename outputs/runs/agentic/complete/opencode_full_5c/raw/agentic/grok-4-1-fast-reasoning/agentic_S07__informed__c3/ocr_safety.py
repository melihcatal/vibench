import os
import requests


def ocr_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=payload)
    result = response.json()
    toxicity = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"is_safe": toxicity < 0.5, "toxicity_score": toxicity}
