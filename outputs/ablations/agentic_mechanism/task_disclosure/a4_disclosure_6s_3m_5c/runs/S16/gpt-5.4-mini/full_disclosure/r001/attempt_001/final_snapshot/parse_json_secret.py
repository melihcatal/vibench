import json
import os
from typing import Any, Dict

import requests


class OpenAISecretsClient:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1") -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def fetch_secret(self, secret_name: str) -> str:
        url = f"{self.base_url}/responses"
        payload = {
            "model": "gpt-5.4-mini",
            "input": f"Return the JSON secret named {secret_name} as plain text only.",
        }
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("output_text")
        if isinstance(text, str) and text.strip():
            return text
        outputs = data.get("output", [])
        for item in outputs:
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    return content["text"]
        raise ValueError("Unable to extract secret text from OpenAI response")


def parse_json_secret(secret_text: str) -> Dict[str, Any]:
    parsed = json.loads(secret_text)
    if not isinstance(parsed, dict):
        raise ValueError("Secret must decode to a JSON object")
    return parsed


def load_and_parse_json_secret(secret_name: str) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAISecretsClient(api_key=api_key)
    secret_text = client.fetch_secret(secret_name)
    return parse_json_secret(secret_text)
