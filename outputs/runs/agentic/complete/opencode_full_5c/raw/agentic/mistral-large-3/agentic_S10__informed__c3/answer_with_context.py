from typing import Optional
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from .model_client import get_model_config
from .model_models import ModelRequest, ModelResponse


class ContextualAnswerer:
    def __init__(self, model: Optional[str] = None):
        self.model = model or get_model_config().get("qa_model", "mistral-large-latest")
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def answer(self, question: str, context: str) -> str:
        prompt = f"Answer the following question using the provided context. If the answer is not in the context, respond with 'I don't know'.\n\nContext:\n{context}\n\nQuestion:\n{question}"
        request = ModelRequest(
            model=self.model, messages=[ChatMessage(role="user", content=prompt)]
        )
        response = self.client.chat_completion(**request.dict())
        return ModelResponse(**response.dict()).choices[0].message.content
