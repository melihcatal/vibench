import json
import requests


def translate_notes(text, target_lang="es", api_key="DUMMY_KEY"):
    url = "https://translation.example.com/v1/translate"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"text": text, "target": target_lang}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        # Assuming response returns translated text in field 'translated'
        return result.get("translated", "")
    else:
        raise Exception("Translation request failed")
