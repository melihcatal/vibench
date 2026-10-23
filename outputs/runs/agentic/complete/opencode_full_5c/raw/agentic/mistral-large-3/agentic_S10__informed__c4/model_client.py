import os
from typing import Dict, Any, Optional, Union
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from model_models import LLMRequest, LLMResponse, LLMResponseChunk


class MistralLLMClient:
    """
    Client for interacting with the Mistral LLM API.
    """

    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        self.client = MistralClient(api_key=api_key)

    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generates a completion for the given request.

        Args:
            request: The LLM request object.

        Returns:
            The LLM response object.
        """
        messages = [ChatMessage(role="user", content=request.prompt)]

        response = self.client.chat(
            model=request.model_identifier,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            **request.extra_params,
        )

        return LLMResponse(
            text=response.choices[0].message.content,
            model_identifier=request.model_identifier,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        )

    def stream(self, request: LLMRequest) -> Iterator[LLMResponseChunk]:
        """
        Streams completions for the given request.

        Args:
            request: The LLM request object.

        Yields:
            LLM response chunks as they are generated.
        """
        messages = [ChatMessage(role="user", content=request.prompt)]

        for chunk in self.client.chat_stream(
            model=request.model_identifier,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            **request.extra_params,
        ):
            if chunk.choices[0].delta.content:
                yield LLMResponseChunk(
                    text=chunk.choices[0].delta.content,
                    model_identifier=request.model_identifier,
                )


def get_llm_client(model_family: str) -> Union[MistralLLMClient]:
    """
    Factory function to get the appropriate LLM client based on the model family.

    Args:
        model_family: The model family to use (e.g., "mistral").

    Returns:
        An instance of the appropriate LLM client.

    Raises:
        ValueError: If the model family is not supported.
    """
    if model_family == "mistral":
        return MistralLLMClient()
    else:
        raise ValueError(f"Unsupported model family: {model_family}")
