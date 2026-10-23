from __future__ import annotations

import os
from typing import Any, Dict, Optional

import openai

from model_models import PlatformRequest, PlatformResponse, StreamChunk


OPENAI_API_BASE = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TTS_MODEL = "tts-1"
DEFAULT_MODERATION_MODEL = "text-moderation-latest"


class OpenAIPlatformClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        project: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 3,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.organization = organization or os.environ.get("OPENAI_ORG_ID")
        self.project = project or os.environ.get("OPENAI_PROJECT_ID")
        self.base_url = base_url or OPENAI_API_BASE
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[openai.OpenAI] = None

    @property
    def client(self) -> openai.OpenAI:
        if self._client is None:
            client_kwargs: Dict[str, Any] = {
                "api_key": self.api_key,
                "base_url": self.base_url,
                "timeout": self.timeout,
                "max_retries": self.max_retries,
            }
            if self.organization:
                client_kwargs["organization"] = self.organization
            if self.project:
                client_kwargs["project"] = self.project
            self._client = openai.OpenAI(**client_kwargs)
        return self._client

    def chat_completion(self, request: PlatformRequest) -> PlatformResponse:
        kwargs: Dict[str, Any] = {
            "model": request.model_id,
            "messages": request.messages,
            "temperature": request.temperature,
            "stream": False,
        }
        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens
        if request.stop is not None:
            kwargs["stop"] = request.stop
        kwargs.update(request.extra_params)

        response = self.client.chat.completions.create(**kwargs)

        content = ""
        finish_reason = None
        if response.choices and len(response.choices) > 0:
            choice = response.choices[0]
            if choice.message and choice.message.content:
                content = choice.message.content
            finish_reason = choice.finish_reason

        return PlatformResponse(
            content=content,
            model_id=response.model,
            finish_reason=finish_reason,
            request_id=response.id,
            usage={
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens
                if response.usage
                else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            },
            raw_response=response,
        )

    def chat_completion_stream(self, request: PlatformRequest):
        kwargs: Dict[str, Any] = {
            "model": request.model_id,
            "messages": request.messages,
            "temperature": request.temperature,
            "stream": True,
        }
        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens
        if request.stop is not None:
            kwargs["stop"] = request.stop
        kwargs.update(request.extra_params)

        stream = self.client.chat.completions.create(**kwargs)

        full_content = []
        last_chunk = None
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                choice = chunk.choices[0]
                delta = choice.delta
                if delta and delta.content:
                    full_content.append(delta.content)
                    yield StreamChunk(
                        content=delta.content,
                        index=choice.index,
                        finish_reason=choice.finish_reason,
                        raw_chunk=chunk,
                    )
                last_chunk = chunk

        return "".join(full_content), last_chunk

    def create_embedding(
        self,
        text: str,
        model: str = DEFAULT_EMBEDDING_MODEL,
        dimensions: Optional[int] = None,
    ):
        kwargs: Dict[str, Any] = {
            "model": model,
            "input": text,
        }
        if dimensions is not None:
            kwargs["dimensions"] = dimensions

        response = self.client.embeddings.create(**kwargs)

        embedding = response.data[0].embedding if response.data else []
        return {
            "embedding": embedding,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            },
            "raw_response": response,
        }

    def create_moderation(
        self,
        text: str,
        model: str = DEFAULT_MODERATION_MODEL,
    ):
        response = self.client.moderations.create(
            model=model,
            input=text,
        )

        result = response.results[0] if response.results else None
        if result:
            return {
                "flagged": result.flagged,
                "categories": dict(result.categories)
                if hasattr(result, "categories")
                else {},
                "category_scores": dict(result.category_scores)
                if hasattr(result, "category_scores")
                else {},
                "raw_response": response,
            }
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "raw_response": response,
        }

    def create_speech(
        self,
        text: str,
        model: str = DEFAULT_TTS_MODEL,
        voice: str = "alloy",
        response_format: str = "mp3",
        speed: float = 1.0,
    ):
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format=response_format,
            speed=speed,
        )

        audio_data = response.content
        return {
            "audio_data": audio_data,
            "model": model,
            "format": response_format,
            "raw_response": response,
        }


def get_platform_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> OpenAIPlatformClient:
    return OpenAIPlatformClient(
        api_key=api_key,
        organization=organization,
        project=project,
    )
