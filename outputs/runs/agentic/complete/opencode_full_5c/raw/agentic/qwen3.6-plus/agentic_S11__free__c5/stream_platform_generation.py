from typing import Optional, List, Dict, Any, Iterator
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk
from model_client import (
    create_openai_client,
    get_default_model,
    get_default_temperature,
    get_default_max_tokens,
)
from model_models import (
    PlatformModelRequest,
    PlatformStreamResponse,
    StreamChunk,
    Message,
    ModelRole,
    normalize_messages,
    build_request_dict,
)


def stream_platform_generation(
    prompt: str,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    stop_sequences: Optional[List[str]] = None,
) -> PlatformStreamResponse:
    if client is None:
        client = create_openai_client()
    target_model = model or get_default_model()
    target_temperature = (
        temperature if temperature is not None else get_default_temperature()
    )
    target_max_tokens = (
        max_tokens if max_tokens is not None else get_default_max_tokens()
    )
    if messages is not None:
        msg_objects = normalize_messages(messages)
    else:
        msg_objects = []
        if system_prompt:
            msg_objects.append(Message(role=ModelRole.SYSTEM, content=system_prompt))
        msg_objects.append(Message(role=ModelRole.USER, content=prompt))
    request = PlatformModelRequest(
        model=target_model,
        messages=msg_objects,
        temperature=target_temperature,
        max_tokens=target_max_tokens,
        stop=stop_sequences,
        stream=True,
    )
    payload = build_request_dict(request)
    stream = client.chat.completions.create(**payload)
    accumulated_content = ""
    chunks: List[StreamChunk] = []
    request_id: Optional[str] = None
    final_model: Optional[str] = None
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    for chunk in stream:
        if request_id is None:
            request_id = chunk.id
        if final_model is None:
            final_model = chunk.model
        if chunk.usage:
            prompt_tokens = chunk.usage.prompt_tokens
            completion_tokens = chunk.usage.completion_tokens
            total_tokens = chunk.usage.total_tokens
        for choice in chunk.choices:
            delta_content = choice.delta.content if choice.delta.content else ""
            finish_reason = choice.finish_reason
            index = choice.index
            accumulated_content += delta_content
            chunks.append(
                StreamChunk(
                    delta=delta_content,
                    finish_reason=finish_reason,
                    index=index,
                )
            )
    return PlatformStreamResponse(
        content=accumulated_content,
        model=final_model or target_model,
        chunks=chunks,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        request_id=request_id,
        raw_response=stream,
    )


def stream_with_callback(
    prompt: str,
    callback,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> PlatformStreamResponse:
    if client is None:
        client = create_openai_client()
    target_model = model or get_default_model()
    target_temperature = (
        temperature if temperature is not None else get_default_temperature()
    )
    target_max_tokens = (
        max_tokens if max_tokens is not None else get_default_max_tokens()
    )
    msg_objects = []
    if system_prompt:
        msg_objects.append(Message(role=ModelRole.SYSTEM, content=system_prompt))
    msg_objects.append(Message(role=ModelRole.USER, content=prompt))
    request = PlatformModelRequest(
        model=target_model,
        messages=msg_objects,
        temperature=target_temperature,
        max_tokens=target_max_tokens,
        stream=True,
    )
    payload = build_request_dict(request)
    stream = client.chat.completions.create(**payload)
    accumulated_content = ""
    chunks: List[StreamChunk] = []
    request_id: Optional[str] = None
    final_model: Optional[str] = None
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    for chunk in stream:
        if request_id is None:
            request_id = chunk.id
        if final_model is None:
            final_model = chunk.model
        if chunk.usage:
            prompt_tokens = chunk.usage.prompt_tokens
            completion_tokens = chunk.usage.completion_tokens
            total_tokens = chunk.usage.total_tokens
        for choice in chunk.choices:
            delta_content = choice.delta.content if choice.delta.content else ""
            finish_reason = choice.finish_reason
            index = choice.index
            accumulated_content += delta_content
            chunk_obj = StreamChunk(
                delta=delta_content,
                finish_reason=finish_reason,
                index=index,
            )
            chunks.append(chunk_obj)
            callback(delta_content, chunk_obj)
    return PlatformStreamResponse(
        content=accumulated_content,
        model=final_model or target_model,
        chunks=chunks,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        request_id=request_id,
        raw_response=stream,
    )


def stream_generator(
    prompt: str,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> Iterator[StreamChunk]:
    if client is None:
        client = create_openai_client()
    target_model = model or get_default_model()
    target_temperature = (
        temperature if temperature is not None else get_default_temperature()
    )
    target_max_tokens = (
        max_tokens if max_tokens is not None else get_default_max_tokens()
    )
    msg_objects = []
    if system_prompt:
        msg_objects.append(Message(role=ModelRole.SYSTEM, content=system_prompt))
    msg_objects.append(Message(role=ModelRole.USER, content=prompt))
    request = PlatformModelRequest(
        model=target_model,
        messages=msg_objects,
        temperature=target_temperature,
        max_tokens=target_max_tokens,
        stream=True,
    )
    payload = build_request_dict(request)
    stream = client.chat.completions.create(**payload)
    for chunk in stream:
        for choice in chunk.choices:
            delta_content = choice.delta.content if choice.delta.content else ""
            finish_reason = choice.finish_reason
            index = choice.index
            yield StreamChunk(
                delta=delta_content,
                finish_reason=finish_reason,
                index=index,
            )
