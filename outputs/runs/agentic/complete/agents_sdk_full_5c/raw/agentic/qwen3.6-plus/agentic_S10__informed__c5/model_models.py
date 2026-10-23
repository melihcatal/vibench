"""
Local helper: Define local request, response, and normalization helpers
for Hosted LLM Inference and Model-Family Selection.

Provider: OpenAI / GPT via OpenAI API
"""

import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable


@dataclass
class CompletionRequest:
    """
    Standardized request model for hosted LLM completions.
    """
    prompt: str
    system_prompt: Optional[str] = None
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    extra_messages: Optional[List[Dict[str, str]]] = None
    json_response: bool = False
    response_format: Optional[Dict[str, Any]] = None

    def to_openai_kwargs(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Convert to kwargs suitable for OpenAI client.chat.completions.create().
        """
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
        }
        if self.json_response:
            kwargs["response_format"] = {"type": "json_object"}
        elif self.response_format:
            kwargs["response_format"] = self.response_format
        return kwargs


@dataclass
class CompletionResponse:
    """
    Standardized response model from a hosted LLM completion.
    """
    text: str
    model_used: str = ""
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw_response: Any = None

    @classmethod
    def from_openai_response(cls, response: Any, raw: Any = None) -> "CompletionResponse":
        """
        Normalize an OpenAI chat completion response into our standard model.
        """
        finish_reason = None
        content = ""
        prompt_tokens = 0
        completion_tokens = 0
        model_used = ""

        if response:
            model_used = response.model or ""
            if response.choices:
                choice = response.choices[0]
                finish_reason = choice.finish_reason
                if choice.message and choice.message.content:
                    content = choice.message.content.strip()
            if response.usage:
                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens
            else:
                total_tokens = prompt_tokens + completion_tokens
        else:
            total_tokens = prompt_tokens + completion_tokens

        return cls(
            text=content,
            model_used=model_used,
            finish_reason=finish_reason,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            raw_response=raw if raw else response,
        )


@dataclass
class StreamChunk:
    """
    Represents a single streaming token chunk.
    """
    content: str
    finish_reason: Optional[str] = None
    accumulated_text: str = ""

    @classmethod
    def from_openai_chunk(cls, chunk: Any, accumulated: str = "") -> "StreamChunk":
        """
        Create a StreamChunk from an OpenAI streaming chunk.
        """
        content = ""
        finish_reason = None
        if chunk and chunk.choices:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                content = delta.content
            finish_reason = chunk.choices[0].finish_reason
        return cls(
            content=content,
            finish_reason=finish_reason,
            accumulated_text=accumulated,
        )


@dataclass
class EmbeddingRequest:
    """
    Standardized request model for embedding generation.
    """
    text: str
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None

    def to_openai_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "input": self.text,
        }
        if self.dimensions:
            kwargs["dimensions"] = self.dimensions
        return kwargs


@dataclass
class EmbeddingResponse:
    """
    Standardized response from an embedding API.
    """
    embedding: List[float]
    model_used: str = ""
    total_tokens: int = 0
    raw_response: Any = None

    @classmethod
    def from_openai_response(cls, response: Any) -> "EmbeddingResponse":
        embedding = []
        model_used = ""
        total_tokens = 0

        if response:
            model_used = response.model or ""
            if response.usage:
                total_tokens = response.usage.total_tokens
            if response.data:
                embedding = response.data[0].embedding

        return cls(
            embedding=embedding,
            model_used=model_used,
            total_tokens=total_tokens,
            raw_response=response,
        )


def parse_json_from_text(text: str) -> Dict[str, Any]:
    """
    Attempt to parse a JSON object from LLM response text.
    Handles cases where the text may be wrapped in markdown code blocks.
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        # Strip leading ```json or ```
        lines = cleaned.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    return json.loads(cleaned)


def build_structured_response_format(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build an OpenAI JSON schema response_format for structured outputs.
    """
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "structured_output",
            "schema": schema,
            "strict": True,
        },
    }
