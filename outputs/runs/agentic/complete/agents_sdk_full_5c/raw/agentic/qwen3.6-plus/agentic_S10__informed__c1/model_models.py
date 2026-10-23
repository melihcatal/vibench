"""
Define local request, response, and normalization helpers for Hosted LLM Inference and Model-Family Selection.
Works with OpenAI Chat Completions and Embeddings responses.
"""

import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Iterator, Union
from openai.types.chat import ChatCompletion, ChatCompletionChunk


@dataclass
class LLMRequest:
    """Normalized request payload for LLM inference."""
    system_prompt: str
    user_prompt: str
    context: Optional[str] = None
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    json_mode: bool = False
    stream: bool = False

    def to_messages(self) -> List[Dict[str, str]]:
        """Convert request to OpenAI message format."""
        messages = [{"role": "system", "content": self.system_prompt}]
        if self.context:
            messages.append({"role": "system", "content": f"Context:\n{self.context}"})
        messages.append({"role": "user", "content": self.user_prompt})
        return messages


@dataclass
class LLMResponse:
    """Normalized response from LLM inference."""
    content: str
    model: str
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw_response: Optional[Any] = None

    @classmethod
    def from_openai_completion(cls, completion: ChatCompletion) -> "LLMResponse":
        """Parse an OpenAI ChatCompletion into a normalized response."""
        choice = completion.choices[0]
        usage = completion.usage
        return cls(
            content=choice.message.content or "",
            model=completion.model,
            finish_reason=choice.finish_reason,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            raw_response=completion,
        )


@dataclass
class StreamingChunk:
    """A single chunk from a streaming LLM response."""
    delta_content: str
    finish_reason: Optional[str] = None

    @classmethod
    def from_openai_chunk(cls, chunk: ChatCompletionChunk) -> Optional["StreamingChunk"]:
        """Parse an OpenAI ChatCompletionChunk into a normalized chunk."""
        if not chunk.choices:
            return None
        choice = chunk.choices[0]
        delta = choice.delta
        if delta is None:
            return None
        return cls(
            delta_content=delta.content or "",
            finish_reason=choice.finish_reason,
        )


def parse_json_response(content: str) -> Dict[str, Any]:
    """Extract and parse JSON from an LLM response string."""
    # Try parsing the raw content first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Try extracting JSON from markdown code blocks
    import re
    json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    # Try finding the first JSON object in the content
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(content[start:end+1])
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Failed to parse JSON from response: {content[:200]}")


def normalize_streaming_output(chunks: Iterator[StreamingChunk]) -> str:
    """Concatenate streaming chunks into a single output string."""
    parts = []
    for chunk in chunks:
        if chunk.delta_content:
            parts.append(chunk.delta_content)
    return "".join(parts)


def build_summary_request(text: str, max_length: int = 150) -> LLMRequest:
    """Build a request for text summarization."""
    return LLMRequest(
        system_prompt="You are a helpful assistant that creates concise summaries.",
        user_prompt=f"Summarize the following text in approximately {max_length} words:\n\n{text}",
        model="gpt-4o",
        temperature=0.3,
    )


def build_json_extraction_request(text: str, schema_description: str) -> LLMRequest:
    """Build a request for structured JSON extraction."""
    return LLMRequest(
        system_prompt=f"Extract structured data from the text and return it as JSON matching this schema: {schema_description}. Return only valid JSON, no explanations.",
        user_prompt=f"Extract structured JSON from the following text:\n\n{text}",
        model="gpt-4o",
        temperature=0.0,
        json_mode=True,
    )


def build_contextual_qa_request(question: str, context: str) -> LLMRequest:
    """Build a request for answering a question with provided context."""
    return LLMRequest(
        system_prompt="You are a helpful assistant. Answer the question using only the provided context. If the answer cannot be found in the context, say so.",
        user_prompt=f"Question: {question}",
        context=context,
        model="gpt-4o",
        temperature=0.2,
    )
