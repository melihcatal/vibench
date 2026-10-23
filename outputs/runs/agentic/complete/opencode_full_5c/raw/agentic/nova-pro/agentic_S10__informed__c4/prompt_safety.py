import requests


def check_safety(text):
    api_key = os.getenv("TISANE_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(
        "https://api.tisane.ai/v1/moderation", headers=headers, json={"input": text}
    )
    return response.json()
