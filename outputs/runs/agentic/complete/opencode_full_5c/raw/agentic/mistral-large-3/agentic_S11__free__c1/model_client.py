from typing import Optional, Dict, Any
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError


class ModelClient:
    """Client helper for Azure AI Inference managed models."""

    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_AI_INFERENCE_ENDPOINT")
        self.key = key or os.getenv("AZURE_AI_INFERENCE_KEY")
        if not self.endpoint or not self.key:
            raise ValueError(
                "Azure AI Inference endpoint and key must be provided or set as environment variables."
            )

        self.client = ChatCompletionsClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    def get_client(self) -> ChatCompletionsClient:
        """Returns the Azure AI Inference client."""
        return self.client

    def prepare_messages(self, system_prompt: str, user_prompt: str) -> list:
        """Prepares messages for Azure AI Inference chat completions."""
        return [SystemMessage(content=system_prompt), UserMessage(content=user_prompt)]
