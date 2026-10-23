import requests


def summarize_translation_quality(translated_text):
    api_key = os.getenv("MISTRAL_API_KEY")
    url = "https://api.mistral.ai/v1/summarize"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"text": translated_text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["summary"]
