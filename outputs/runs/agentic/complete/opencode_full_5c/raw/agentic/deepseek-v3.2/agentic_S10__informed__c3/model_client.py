import os
from openai import OpenAI
from typing import Optional


class ModelClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.base_url = base_url or os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def get_client(self) -> OpenAI:
        return self.client

    def get_default_model(self) -> str:
        return os.getenv("OPENAI_MODEL", "gpt-4o")

    def create_completion(self, messages, model: Optional[str] = None, **kwargs):
        model = model or self.get_default_model()
        return self.client.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
