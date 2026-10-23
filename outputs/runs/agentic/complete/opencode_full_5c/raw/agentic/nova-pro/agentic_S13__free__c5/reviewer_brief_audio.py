import requests


def generate_reviewer_brief(text: str) -> str:
    api_key = "YOUR_AUDIO_GENERATION_API_KEY"
    api_url = "https://api.audioprovider.com/generate"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"text": text}
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["audio_url"]
