import os
from typing import Any, Dict

import requests


class MicrosoftTranslatorClient:
    def __init__(self, api_key: str = None, region: str = None, endpoint: str = None):
        self.api_key = api_key or os.environ.get("MICROSOFT_TRANSLATOR_API_KEY", "")
        self.region = region or os.environ.get("MICROSOFT_TRANSLATOR_REGION", "")
        self.endpoint = endpoint or os.environ.get("MICROSOFT_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")

    def translate(self, text: str, source_language: str, target_language: str) -> Dict[str, Any]:
        response = requests.post(
            f"{self.endpoint}/translate",
            headers={
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Ocp-Apim-Subscription-Region": self.region,
            },
            params={"api-version": "3.0", "from": source_language, "to": target_language},
            json=[{"Text": text}],
            timeout=30,
        )
        response.raise_for_status()
        return response.json()[0]["translations"][0]
