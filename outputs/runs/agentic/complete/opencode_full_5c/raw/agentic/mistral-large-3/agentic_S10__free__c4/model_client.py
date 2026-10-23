import os
from typing import Optional, Dict, Any, Union
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from model_models import (
    SummarizationRequest,
    SummarizationResponse,
    ExtractionRequest,
    ExtractionResponse,
    QARequest,
    QAResponse,
    CompletionRequest,
    CompletionResponse,
)


class LLMClient:
    """
    Client helper for interacting with the Mistral AI hosted LLM service.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        self.client = MistralClient(api_key=self.api_key)

    def summarize(self, request: SummarizationRequest) -> SummarizationResponse:
        messages = [
            ChatMessage(
                role="system",
                content="You are a helpful assistant that summarizes text.",
            ),
            ChatMessage(
                role="user",
                content=f"Summarize the following text in {request.max_tokens} tokens or less:\n\n{request.input_text}",
            ),
        ]

        response = self.client.chat(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        return SummarizationResponse(summary=response.choices[0].message.content)

    def extract(self, request: ExtractionRequest) -> ExtractionResponse:
        schema_description = json.dumps(request.json_schema, indent=2)
        messages = [
            ChatMessage(
                role="system",
                content=f"You are a helpful assistant that extracts structured JSON from text. The JSON must conform to this schema:\n{schema_description}",
            ),
            ChatMessage(
                role="user",
                content=f"Extract JSON from the following text:\n\n{request.input_text}",
            ),
        ]

        response = self.client.chat(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        extracted_data = json.loads(response.choices[0].message.content)
        return ExtractionResponse(extracted_data=extracted_data)

    def answer(self, request: QARequest) -> QAResponse:
        messages = [
            ChatMessage(
                role="system",
                content="You are a helpful assistant that answers questions using provided context.",
            ),
            ChatMessage(
                role="user",
                content=f"Context:\n{request.context}\n\nQuestion: {request.question}",
            ),
        ]

        response = self.client.chat(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        return QAResponse(answer=response.choices[0].message.content)

    def stream_completion(self, request: CompletionRequest) -> Iterator[str]:
        messages = [
            ChatMessage(
                role="system",
                content="You are a helpful assistant that generates text based on prompts.",
            ),
            ChatMessage(role="user", content=request.prompt),
        ]

        response = self.client.chat_stream(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


def get_llm_client() -> LLMClient:
    """
    Factory function to create and return an LLMClient instance.
    """
    return LLMClient()


import json
