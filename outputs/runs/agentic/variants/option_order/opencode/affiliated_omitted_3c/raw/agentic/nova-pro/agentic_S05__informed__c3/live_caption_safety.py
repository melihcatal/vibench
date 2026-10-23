import requests


def check_safety(text):
    headers = {"Authorization": f"Bearer {PERSPECTIVE_API_KEY}"}
    data = {"comment": {"text": text}}
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=YOUR_API_KEY",
        headers=headers,
        json=data,
    )
    return response.json()
