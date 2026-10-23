import json
from typing import List, Dict, Any

# Azure OpenAI request/response shapes (simplified for demo)


class ModelInvocationRequest:
    """
    Request shape used throughout the Managed Model Platform workflow.
    """

    def __init__(
        self,
        deployment_id: str,
        messages: List[Dict[str, Any]],
        temperature: float = 0.0,
    ):
        self.deployment_id = deployment_id
        self.messages = messages
        self.temperature = temperature

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelInvocationRequest":
        return cls(**data)


class ModelInvocationResponse:
    """
    Normalized response container used downstream.
    """

    def __init__(
        self, model: str, choices: List[Dict[str, Any]], usage: Dict[str, int]
    ):
        self.model = model
        self.choices = choices
        self.usage = usage

    @classmethod
    def from_sdk(cls, sdk_resp):  # azure openai SDK response
        return cls(
            model=sdk_resp.model,
            choices=sdk_resp.choices,
            usage=sdk_resp.usage,  # dict with prompt_tokens, completion_tokens etc.
        )


class ModelGenerationResponse(ModelInvocationResponse):
    """Same shape as ModelInvocationResponse, used by streaming helpers."""

    pass
