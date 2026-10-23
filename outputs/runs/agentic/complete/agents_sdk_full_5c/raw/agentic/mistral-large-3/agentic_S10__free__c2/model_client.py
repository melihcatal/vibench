import os
import requests
from typing import Optional
from pydantic import BaseSettings


class LLMSettings(BaseSettings):
    together_api_key: Optional[str] = os.getenv("TOGETHER_API_KEY")
    timeout: int = 30


class LLMClient:
    def __init__(self, settings: LLMSettings):
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.settings.together_api_key}",
            "Content-Type": "application/json"
        })

    def post(self, url: str, json: dict, **kwargs):
        return self.session.post(url, json=json, timeout=self.settings.timeout, **kwargs)


def get_llm_client() -> LLMClient:
    settings = LLMSettings()
    return LLMClient(settings)