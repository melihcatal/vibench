from typing import Optional

import requests


def localized_platform_output(text: str, target_language: str = "es", endpoint: Optional[str] = None, api_key: Optional[str] = None) -> str:
    endpoint = (endpoint or __import__("os").environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")).rstrip("/")
    region = __import__("os").environ.get("AZURE_TRANSLATOR_REGION", "")
    api_key = api_key or __import__("os").environ.get("AZURE_TRANSLATOR_KEY", "")
    url = f"{endpoint}/translate?api-version=3.0&to={target_language}"
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    if region:
        headers["Ocp-Apim-Subscription-Region"] = region
    response = requests.post(url, headers=headers, json=[{"text": text}], timeout=30)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
