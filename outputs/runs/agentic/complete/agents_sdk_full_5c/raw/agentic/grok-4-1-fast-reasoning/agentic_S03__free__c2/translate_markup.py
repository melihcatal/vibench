import os
import requests
from typing import Optional

def translate_markup(markup: str, source_lang: Optional[str] = None, target_lang: str) -> str:
    endpoint = "https://api.cognitive.microsofttranslator.com"
    params = {
        "api-version": "3.0",
        "from": source_lang,
        "to": [target_lang],
        "textType": "html"
    }
    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv("AZURE_TRANSLATOR_KEY"),
        "Ocp-Apim-Subscription-Region": os.getenv("AZURE_TRANSLATOR_REGION", "global"),
        "Content-Type": "application/json"
    }
    body = [{"Text": markup}]
    response = requests.post(f"{endpoint}/translate", params=params, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
