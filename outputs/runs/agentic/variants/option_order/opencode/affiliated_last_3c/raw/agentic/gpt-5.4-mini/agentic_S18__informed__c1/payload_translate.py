import os
import requests


def translate_payload_text(text: str, target_language: str) -> dict:
    endpoint = (
        os.environ["AZURE_TRANSLATOR_ENDPOINT"].rstrip("/")
        if os.getenv("AZURE_TRANSLATOR_ENDPOINT")
        else "https://api.cognitive.microsofttranslator.com"
    )
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ.get("AZURE_TRANSLATOR_REGION", "")
    url = f"{endpoint}/translate?api-version=3.0&to={target_language}"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    if region:
        headers["Ocp-Apim-Subscription-Region"] = region
    response = requests.post(url, headers=headers, json=[{"Text": text}], timeout=30)
    response.raise_for_status()
    data = response.json()
    translated = data[0]["translations"][0]["text"] if data else ""
    return {
        "provider": "azure-ai-translator",
        "source_text": text,
        "translated_text": translated,
        "target_language": target_language,
    }
