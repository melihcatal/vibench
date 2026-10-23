import requests


def moderate_transcript(transcript):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer TISANE_API_KEY",
    }
    data = {"text": transcript}
    response = requests.post(
        "https://api.tisane.ai/v1/moderate", headers=headers, json=data
    )
    return response.json()["moderation_results"]
