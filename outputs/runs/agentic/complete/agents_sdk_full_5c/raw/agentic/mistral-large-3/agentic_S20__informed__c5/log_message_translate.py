from typing import List, Dict
import os
import requests


def translate_log_messages(messages: List[str], target_language: str = "es") -> List[Dict[str, str]]:
    api_key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    url = f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }
    body = [{"text": message} for message in messages]
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return [{"original": msg, "translated": result["translations"][0]["text"]} for msg, result in zip(messages, response.json())]
    else:
        return [{"original": msg, "translated": ""} for msg in messages]