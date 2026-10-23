import requests


def quality_summary(text):
    api_key = os.getenv("MISTRAL_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(
        "https://api.mistral.ai/v1/quality-summary",
        headers=headers,
        json={"text": text},
    )
    return response.json()
