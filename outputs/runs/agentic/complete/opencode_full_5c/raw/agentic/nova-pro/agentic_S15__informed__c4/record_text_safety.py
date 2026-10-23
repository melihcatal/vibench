import requests

TISANE_API_KEY = os.getenv("TISANE_API_KEY")
TISANE_ENDPOINT = "https://api.tisane.com/v1/moderation"


def check_safety(text):
    headers = {"Authorization": f"Bearer {TISANE_API_KEY}"}
    data = {"text": text}
    response = requests.post(TISANE_ENDPOINT, headers=headers, json=data)
    return response.json()
