import json
from typing import Dict, Any, Union, List

class LLMResponse:
    """Normalized wrapper around responses from different LLM providers.
    Supports OpenAI-like structure and can be extended for other services.
    """
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def from_openai(cls, resp):
        """Create a normalized response from an OpenAI SDK response object."""
        # OpenAI's chat.completions response shape
        choice = resp.choices[0]
        message = choice.message
        return cls({
            "id": choice.id,
            "choices": [{
                "message": {
                    "role": message.role,
                    "content": message.content
                }
            }]
        })

    def get_content(self) -> str:
        """Return the textual content of the first assistant message."""
        return self.data["choices"][0]["message"]["content"]

    def to_dict(self) -> Dict[str, Any]:
        return self.data

    @staticmethod
    def from_dict(raw: Dict[str, Any]) -> "LLMResponse":
        return LLMResponse(raw)


class LLMRequest:
    """Standardized request payload for LLM calls.",
    def __init__(self, model: str, messages: List[Dict[str, Any]], **kwargs):
        self.model = model
        self.messages = messages
        self.kwargs = kwargs

    def to_openai_dict(self) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": self.messages,
        }
        payload.update(self.kwargs)
        return payload

    @classmethod
    def from_user_input(cls, prompt: str, **kwargs):
        messages = [{"role": "user", "content": prompt}]
        return cls(None, messages, **kwargs)
