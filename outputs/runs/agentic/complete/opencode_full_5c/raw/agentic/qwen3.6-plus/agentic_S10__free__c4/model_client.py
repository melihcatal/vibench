import os
from typing import Optional, Generator, Any
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk
from openai.types import CreateEmbeddingResponse, ModerationCreateResponse

from model_models import (
    LLMRequest,
    LLMResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    ModerationRequest,
    ModerationResponse,
    ModerationResult,
    StreamChunk,
    build_completion_payload,
    build_embedding_payload,
    extract_text_from_response,
    parse_stream_chunk,
)

OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL_FAMILY_PREFIX = "gpt-4o"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or get_openai_api_key()
    return OpenAI(api_key=key, base_url=OPENAI_API_BASE)


def load_config() -> dict[str, str]:
    return {
        "api_key": get_openai_api_key(),
        "base_url": OPENAI_API_BASE,
        "default_model": "gpt-4o-mini",
        "embedding_model": "text-embedding-3-small",
        "moderation_model": "omni-moderation-latest",
        "tts_model": "tts-1",
    }


def normalize_llm_request(request: LLMRequest) -> dict[str, Any]:
    return build_completion_payload(request)


def parse_llm_response(response: Any) -> LLMResponse:
    content = extract_text_from_response(response)
    usage = {}
    finish_reason = None
    model = "gpt-4o-mini"
    if hasattr(response, "usage") and response.usage:
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    if hasattr(response, "model") and response.model:
        model = response.model
    if hasattr(response, "choices") and response.choices:
        finish_reason = response.choices[0].finish_reason
    return LLMResponse(
        content=content,
        model=model,
        usage=usage,
        finish_reason=finish_reason,
    )


def parse_embedding_response(response: CreateEmbeddingResponse) -> EmbeddingResponse:
    embeddings = [item.embedding for item in response.data]
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    return EmbeddingResponse(
        embeddings=embeddings,
        model=response.model,
        usage=usage,
    )


def parse_moderation_response(response: ModerationCreateResponse) -> ModerationResponse:
    results = []
    for item in response.results:
        categories = {}
        category_scores = {}
        if hasattr(item, "categories"):
            categories = dict(item.categories)
        if hasattr(item, "category_scores"):
            category_scores = dict(item.category_scores)
        results.append(
            ModerationResult(
                flagged=item.flagged,
                categories=categories,
                category_scores=category_scores,
            )
        )
    return ModerationResponse(results=results, model=response.model)


def stream_chunks(
    client: OpenAI, request: LLMRequest
) -> Generator[StreamChunk, None, None]:
    payload = build_completion_payload(request)
    payload["stream"] = True
    stream = client.chat.completions.create(**payload)
    for chunk in stream:
        parsed = parse_stream_chunk(chunk)
        if parsed is not None:
            yield parsed


def execute_completion(client: OpenAI, request: LLMRequest) -> LLMResponse:
    payload = build_completion_payload(request)
    response = client.chat.completions.create(**payload)
    return parse_llm_response(response)


def execute_embedding(client: OpenAI, request: EmbeddingRequest) -> EmbeddingResponse:
    payload = build_embedding_payload(request)
    response = client.embeddings.create(**payload)
    return parse_embedding_response(response)


def execute_moderation(
    client: OpenAI, request: ModerationRequest
) -> ModerationResponse:
    response = client.moderations.create(input=request.input, model=request.model)
    return parse_moderation_response(response)
