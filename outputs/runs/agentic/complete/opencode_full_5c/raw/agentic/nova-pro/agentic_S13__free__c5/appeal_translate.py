import requests


def translate_appeal(text: str, target_language: str) -> str:
    api_key = "YOUR_TRANSLATION_API_KEY"
    api_url = "https://api.translationprovider.com/translate"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"text": text, "target": target_language}
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["translated_text"]
