"""
Local request, response, and normalization helpers for Hosted LLM Inference
and Model-Family Selection using the OpenAI Chat Completions API.

Provider: OpenAI / Azure OpenAI
SDK: openai
Auth: OPENAI_API_KEY
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LLMRequest:
    """Standardized request payload for hosted LLM inference."""
    user_prompt: str
    system_prompt: Optional[str] = None
    model_name: Optional[str] = "gpt-4o"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2048
    json_mode: bool = False
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UsageInfo:
    """Token usage information returned by the OpenAI API."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class LLMResponse:
    """Standardized response from hosted LLM inference."""
    content: str = ""
    model: str = ""
    finish_reason: str = ""
    usage: Optional[UsageInfo] = None


def normalize_openai_completion(completion: Any) -> LLMResponse:
    """
    Normalize an OpenAI ChatCompletion response into an LLMResponse.

    Provider: OpenAI Chat Completions API (api.openai.com/v1/chat/completions)
    Concrete models: gpt-4o, gpt-4o-mini, gpt-4-turbo
    """
    choice = completion.choices[0]
    message = choice.message
    usage_data = completion.usage

    usage = UsageInfo(
        prompt_tokens=usage_data.prompt_tokens if usage_data else 0,
        completion_tokens=usage_data.completion_tokens if usage_data else 0,
        total_tokens=usage_data.total_tokens if usage_data else 0,
    )

    return LLMResponse(
        content=message.content or "",
        model=completion.model or "",
        finish_reason=choice.finish_reason or "",
        usage=usage,
    )


def normalize_openai_stream_delta(chunk: Any) -> Optional[str]:
    """
    Extract delta text from an OpenAI streaming chunk.

    Provider: OpenAI Chat Completions API streaming
    """
    if not chunk.choices:
        return None
    delta = chunk.choices[0].delta
    return delta.content if delta.content else None


def build_summarization_request(
    text: str,
    max_words: int = 150,
    model_name: str = "gpt-4o-mini",
) -> LLMRequest:
    """Build an LLMRequest optimized for text summarization."""
    return LLMRequest(
        user_prompt=text,
        system_prompt=(
            f"You are a concise summarizer. Summarize the following text "
            f"in approximately {max_words} words or fewer. "
            f"Focus on the key points and main conclusions."
        ),
        model_name=model_name,
        temperature=0.3,
        max_tokens=1024,
    )


def build_json_extraction_request(
    text: str,
    schema_description: str,
    model_name: str = "gpt-4o",
) -> LLMRequest:
    """Build an LLMRequest optimized for structured JSON extraction."""
    return LLMRequest(
        user_prompt=text,
        system_prompt=(
            f"Extract structured data from the following text. "
            f"Return ONLY valid JSON matching this description: {schema_description}. "
            f"Do not include any markdown formatting or additional text. "
            f"Return a single JSON object."
        ),
        model_name=model_name,
        temperature=0.1,
        max_tokens=2048,
        json_mode=True,
    )


def build_context_qa_request(
    context: str,
    question: str,
    model_name: str = "gpt-4o",
) -> LLMRequest:
    """Build an LLMRequest for answering questions with provided context."""
    return LLMRequest(
        user_prompt=f"Context:\n{context}\n\nQuestion: {question}",
        system_prompt=(
            "Answer the user's question using ONLY the provided context. "
            "If the context does not contain enough information to answer, "
            "say so explicitly. Be concise and direct."
        ),
        model_name=model_name,
        temperature=0.3,
        max_tokens=1024,
    )
