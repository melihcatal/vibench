"""
Define local request, response, and normalization helpers for Hosted LLM Inference and Model-Family Selection.
Provider: OpenAI - https://platform.openai.com
"""

import json
import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Iterator


@dataclass
class LLMRequest:
    """Normalized request payload for hosted LLM inference via OpenAI."""
    model: str
    messages: List[Dict[str, str]]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    stop_sequences: Optional[List[str]] = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    response_format: Optional[Dict[str, Any]] = None
    stream: bool = False

    def to_openai_kwargs(self) -> Dict[str, Any]:
        """Convert to keyword arguments for openai.OpenAI.chat.completions.create."""
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stream": self.stream,
        }
        if self.stop_sequences:
            kwargs["stop"] = self.stop_sequences
        if self.response_format:
            kwargs["response_format"] = self.response_format
        return kwargs


@dataclass
class LLMResponse:
    """Normalized response from a hosted LLM via OpenAI."""
    text: str
    model: str
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw_response: Optional[Any] = None

    @classmethod
    def from_openai(cls, response: Any, model: str) -> "LLMResponse":
        """Parse an OpenAI chat completion response into a normalized LLMResponse."""
        choice = response.choices[0]
        content = choice.message.content or ""

        usage = response.usage
        return cls(
            text=content,
            model=model,
            finish_reason=choice.finish_reason,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            raw_response=response,
        )


@dataclass
class StreamChunk:
    """A single chunk from a streaming OpenAI completion."""
    text: str
    finish_reason: Optional[str] = None
    raw_chunk: Optional[Any] = None


def normalize_system_user_messages(
    system_prompt: str,
    user_prompt: str,
) -> List[Dict[str, str]]:
    """Create a standard OpenAI chat messages list with system and user roles."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    return messages


def normalize_messages_with_context(
    system_prompt: str,
    context: str,
    question: str,
) -> List[Dict[str, str]]:
    """Build messages for a context-grounded QA via OpenAI chat."""
    user_content = f"Context:\n{context}\n\nQuestion: {question}"
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": user_content})
    return messages


def parse_json_from_text(text: str) -> Dict[str, Any]:
    """
    Attempt to extract and parse a JSON object from LLM output text.
    Handles cases where the model wraps JSON in markdown code fences.
    """
    stripped = text.strip()
    # Try to strip markdown JSON code fences
    json_block_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", stripped, re.DOTALL)
    if json_block_match:
        stripped = json_block_match.group(1).strip()

    # Try direct parse
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    # Try to find a JSON object by scanning for balanced braces
    start_idx = stripped.find("{")
    if start_idx != -1:
        brace_count = 0
        end_idx = start_idx
        for i in range(start_idx, len(stripped)):
            if stripped[i] == "{":
                brace_count += 1
            elif stripped[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
        candidate = stripped[start_idx:end_idx]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from LLM output:\n{text}")


def chunk_stream_from_openai(
    openai_stream: Iterator[Any],
) -> Iterator[StreamChunk]:
    """Iterate over an OpenAI streaming response and yield normalized StreamChunks."""
    for chunk in openai_stream:
        for choice in chunk.choices:
            delta = choice.delta
            text = delta.content if delta and delta.content else ""
            finish = choice.finish_reason
            if text or finish:
                yield StreamChunk(
                    text=text,
                    finish_reason=finish,
                    raw_chunk=chunk,
                )
