import os
from typing import Dict, Any, Optional, Iterator

import dashscope
from dashscope import Generation
from dashscope.api_entities.dashscope_response import GenerationResponse

from model_models import LLMRequest, LLMResponse


class DashScopeClient:
    """Client for DashScope Qwen API."""

    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")
        dashscope.api_key = self.api_key

    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion for the given request."""
        response = Generation.call(
            model=request.model_id,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            result_format="message",
        )

        if response.status_code != 200:
            raise RuntimeError(f"API request failed: {response.message}")

        text = response.output.choices[0].message.content
        return LLMResponse(text=text)

    def stream(self, request: LLMRequest) -> Iterator[LLMResponse]:
        """Stream completions for the given request."""
        responses = Generation.call(
            model=request.model_id,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            result_format="message",
            stream=True,
        )

        for response in responses:
            if response.status_code != 200:
                raise RuntimeError(f"API request failed: {response.message}")
            text = response.output.choices[0].message.content
            yield LLMResponse(text=text)


def get_llm_client() -> DashScopeClient:
    """Factory method to get the LLM client."""
    return DashScopeClient()
