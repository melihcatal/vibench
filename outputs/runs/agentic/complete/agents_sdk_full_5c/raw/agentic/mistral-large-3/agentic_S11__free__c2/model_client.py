import os
from typing import Optional
import cohere
from cohere import Client
from model_models import ModelRequest

class ModelClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Cohere API key not provided.")
        self.client = Client(self.api_key)

    def chat(self, model: str, message: str, temperature: float, max_tokens: int) -> cohere.ChatResponse:
        return self.client.chat(
            model=model,
            message=message,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def chat_stream(self, model: str, message: str, temperature: float, max_tokens: int):
        return self.client.chat_stream(
            model=model,
            message=message,
            temperature=temperature,
            max_tokens=max_tokens,
        )

def get_model_client() -> ModelClient:
    return ModelClient()