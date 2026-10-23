import os
from typing import Any, AsyncGenerator, Dict, List, Union

import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from model_models import (
    ChatCompletionRequest,
    ChatPrompt,
    EmbeddingRequest,
    EmbeddingResponse,
    LLMResponse,
    StreamChunk,
    TextCompletionRequest,
)


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

    def _get_generation_config(
        self, request: Union[TextCompletionRequest, ChatCompletionRequest]
    ) -> GenerationConfig:
        return GenerationConfig(
            max_output_tokens=request.max_output_tokens,
            temperature=request.temperature,
        )

    def _get_model(self, model_name: str):
        return genai.GenerativeModel(model_name=model_name)

    def text_completion(self, request: TextCompletionRequest) -> LLMResponse:
        model = self._get_model(request.model_name)
        generation_config = self._get_generation_config(request)
        response = model.generate_content(
            request.prompt,
            generation_config=generation_config,
        )
        return LLMResponse.from_gemini_response(response)

    def chat_completion(self, request: ChatCompletionRequest) -> LLMResponse:
        model = self._get_model(request.model_name)
        generation_config = self._get_generation_config(request)
        chat_history = [p.to_gemini_format() for p in request.history]
        # For chat completion, Gemini API expects content list for history, not a single string
        # The first message should be 'user' role to initiate conversation

        # Initialize chat with the first message, if history is not empty
        if chat_history:
            # Assuming the last message in history is the current user prompt
            initial_message_content = chat_history[-1]["parts"][0]["text"]
            chat_session = model.start_chat(
                history=chat_history[:-1] if len(chat_history) > 1 else []
            )
            response = chat_session.send_message(
                initial_message_content,
                generation_config=generation_config,
            )
        else:
            raise ValueError("ChatCompletionRequest history cannot be empty.")

        return LLMResponse.from_gemini_response(response)

    async def stream_completion(
        self, request: TextCompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        model = self._get_model(request.model_name)
        generation_config = self._get_generation_config(request)
        responses = model.generate_content(
            request.prompt,
            generation_config=generation_config,
            stream=True,
        )
        for response in responses:
            yield StreamChunk.from_gemini_chunk(response)

    def embed_content(self, request: EmbeddingRequest) -> EmbeddingResponse:
        model = self._get_model(request.model_name)
        if isinstance(request.text, list):
            response = model.embed_content(content=request.text)
        else:
            response = model.embed_content(content=request.text)

        return EmbeddingResponse.from_gemini_response(response)
