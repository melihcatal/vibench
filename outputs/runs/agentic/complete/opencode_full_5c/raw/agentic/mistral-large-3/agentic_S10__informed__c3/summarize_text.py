from typing import Optional, Dict, Any
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from .model_client import get_model_config
from .model_models import ModelRequest, ModelResponse


class TextSummarizer:
    def __init__(self, model: Optional[str] = None):
        self.model = model or get_model_config().get(
            "summarization_model", "mistral-large-latest"
        )
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def summarize(self, text: str, max_tokens: int = 150) -> str:
        request = ModelRequest(
            model=self.model,
            messages=[
                ChatMessage(
                    role="user",
                    content=f"Summarize the following text in a concise manner:\n\n{text}",
                )
            ],
            max_tokens=max_tokens,
        )
        response = self.client.chat_completion(**request.dict())
        return ModelResponse(**response.dict()).choices[0].message.content
