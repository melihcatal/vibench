from typing import Optional, Dict, Any
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from .model_client import get_model_config
from .model_models import ModelRequest, ModelResponse


class JSONExtractor:
    def __init__(self, model: Optional[str] = None):
        self.model = model or get_model_config().get(
            "extraction_model", "mistral-large-latest"
        )
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def extract(self, text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        schema_description = "\n".join(
            [f"- {key}: {value}" for key, value in schema.items()]
        )
        prompt = f"Extract the following fields from the text below and return them as a valid JSON object:\n\n{schema_description}\n\nText:\n{text}"
        request = ModelRequest(
            model=self.model,
            messages=[ChatMessage(role="user", content=prompt)],
            response_format={"type": "json_object"},
        )
        response = self.client.chat_completion(**request.dict())
        return ModelResponse(**response.dict()).choices[0].message.content
