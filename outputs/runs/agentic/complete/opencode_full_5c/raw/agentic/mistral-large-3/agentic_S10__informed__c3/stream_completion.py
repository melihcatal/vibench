from typing import Optional, Iterator
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from .model_client import get_model_config
from .model_models import ModelRequest, ModelResponse


class CompletionStreamer:
    def __init__(self, model: Optional[str] = None):
        self.model = model or get_model_config().get(
            "streaming_model", "mistral-large-latest"
        )
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def stream(self, prompt: str) -> Iterator[str]:
        request = ModelRequest(
            model=self.model,
            messages=[ChatMessage(role="user", content=prompt)],
            stream=True,
        )
        stream = self.client.chat_stream(**request.dict())
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
