import os
from typing import Optional, Iterator
import cohere
from model_models import ModelRequest, ModelResponse

class ModelClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Cohere API key not provided")
        self.client = cohere.Client(self.api_key)

    def chat(self, model: str, message: str, temperature: float, max_tokens: int) -> ModelResponse:
        response = self.client.chat(
            model=model,
            message=message,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return ModelResponse(
            text=response.text,
            model=response.model,
            response_id=response.response_id,
            meta=response.meta,
        )

    def chat_stream(self, model: str, message: str, temperature: float, max_tokens: int) -> Iterator[ModelResponse]:
        stream = self.client.chat_stream(
            model=model,
            message=message,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        for event in stream:
            if event.event_type == "text-generation":
                yield ModelResponse(
                    text=event.text,
                    model=model,
                    response_id=None,
                    meta=None,
                )

def get_model_client() -> ModelClient:
    return ModelClient()