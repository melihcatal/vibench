import os
from typing import Optional, Dict, Any, Union

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


class ModelClient:
    """Client for Mistral Chat API."""

    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        self.client = MistralClient(api_key=self.api_key)

    def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send chat completion request to Mistral API."""
        messages = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in request["messages"]
        ]
        response = self.client.chat(
            model=request["model"],
            messages=messages,
            max_tokens=request.get("max_tokens"),
            temperature=request.get("temperature"),
            top_p=request.get("top_p"),
            safe_prompt=request.get("safe_prompt", False),
        )
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": choice.message.content,
                    }
                }
                for choice in [response]
            ]
        }

    def stream_chat_completion(
        self, request: Dict[str, Any]
    ) -> Iterator[Dict[str, Any]]:
        """Stream chat completion responses from Mistral API."""
        messages = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in request["messages"]
        ]
        response_stream = self.client.chat_stream(
            model=request["model"],
            messages=messages,
            max_tokens=request.get("max_tokens"),
            temperature=request.get("temperature"),
            top_p=request.get("top_p"),
            safe_prompt=request.get("safe_prompt", False),
        )

        for chunk in response_stream:
            if chunk.choices[0].delta.content:
                yield {
                    "choices": [
                        {
                            "delta": {
                                "role": "assistant",
                                "content": chunk.choices[0].delta.content,
                            }
                        }
                    ]
                }


def get_model_client() -> ModelClient:
    """Get configured Mistral API client."""
    return ModelClient()
