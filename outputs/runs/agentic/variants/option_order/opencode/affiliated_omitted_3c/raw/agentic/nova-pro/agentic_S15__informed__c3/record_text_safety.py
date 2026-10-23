import os
import requests


def check_text_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(
        "https://api.perspectiveapi.com/v1/comment", headers=headers, json=data
    )
    return response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] < 0.5
