import os
from typing import Dict, Any, Iterator
import google.generativeai as genai
from google.generativeai.types import GenerationConfig, Tool
from model_models import (
    LLMRequest,
    LLMResponse,
    LLMStreamResponse,
    EmbeddingRequest,
    EmbeddingResponse,
)


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

    def _get_generation_config(self, request: LLMRequest) -> GenerationConfig:
        return GenerationConfig(
            max_output_tokens=request.max_output_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
        )

    def generate_text(self, request: LLMRequest) -> LLMResponse:
        model = genai.GenerativeModel(model_name=request.model_family)
        generation_config = self._get_generation_config(request)
        contents = [request.prompt]
        if request.context:
            contents.insert(0, request.context)

        response = model.generate_content(
            contents,
            generation_config=generation_config,
            tools=[Tool.from_json(request.json_schema)]
            if request.json_schema
            else None,
            safety_settings=os.getenv(
                "GEMINI_SAFETY_SETTINGS_THRESHOLD"
            ),  # Placeholder for safety settings, usually set at model config level
        )
        return LLMResponse(
            text=response.text,
            metadata={
                "model_family": request.model_family,
                "prompt_feedback": response.prompt_feedback.to_dict()
                if response.prompt_feedback
                else None,
                "finish_reason": response.candidates[0].finish_reason.name
                if response.candidates
                else None,
            },
        )

    def stream_text(self, request: LLMRequest) -> Iterator[LLMStreamResponse]:
        model = genai.GenerativeModel(model_name=request.model_family)
        generation_config = self._get_generation_config(request)
        contents = [request.prompt]
        if request.context:
            contents.insert(0, request.context)

        response_stream = model.generate_content(
            contents,
            generation_config=generation_config,
            stream=True,
            tools=[Tool.from_json(request.json_schema)]
            if request.json_schema
            else None,
            safety_settings=os.getenv(
                "GEMINI_SAFETY_SETTINGS_THRESHOLD"
            ),  # Placeholder for safety settings, usually set at model config level
        )
        for chunk in response_stream:
            yield LLMStreamResponse(
                chunk=chunk.text,
                metadata={
                    "model_family": request.model_family,
                    "finish_reason": chunk.candidates[0].finish_reason.name
                    if chunk.candidates
                    else None,
                },
            )

    def embed_text(self, request: EmbeddingRequest) -> EmbeddingResponse:
        model = genai.GenerativeModel(model_name=request.model_family)
        response = genai.embed_content(
            model=request.model_family,
            content=request.text,
        )
        return EmbeddingResponse(
            embedding=response["embedding"],
            metadata={
                "model_family": request.model_family,
            },
        )
