from typing import Optional, List, Dict, Any
from openai import OpenAI
from openai.types.chat import ChatCompletion
from model_client import (
    create_openai_client,
    get_default_model,
    get_default_temperature,
    get_default_max_tokens,
)
from model_models import (
    PlatformModelRequest,
    PlatformModelResponse,
    Message,
    ModelRole,
    normalize_messages,
    build_request_dict,
)


def invoke_platform_model(
    prompt: str,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    stop_sequences: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> PlatformModelResponse:
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
        stream=False,
        seed=seed,
    )
    payload = build_request_dict(request)
    response: ChatCompletion = client.chat.completions.create(**payload)
    choice = response.choices[0]
    content = choice.message.content if choice.message.content else ""
    usage = response.usage
    return PlatformModelResponse(
        content=content,
        model=response.model,
        finish_reason=choice.finish_reason,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        request_id=response.id,
        raw_response=response,
    )


def invoke_with_request_object(
    request: PlatformModelRequest,
    client: Optional[OpenAI] = None,
) -> PlatformModelResponse:
    if client is None:
        client = create_openai_client()
    payload = build_request_dict(request)
    response: ChatCompletion = client.chat.completions.create(**payload)
    choice = response.choices[0]
    content = choice.message.content if choice.message.content else ""
    usage = response.usage
    return PlatformModelResponse(
        content=content,
        model=response.model,
        finish_reason=choice.finish_reason,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        request_id=response.id,
        raw_response=response,
    )


def invoke_with_resource(
    prompt: str,
    resource_id: str,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> PlatformModelResponse:
    if client is None:
        client = create_openai_client()
    target_model = resource_id
    target_temperature = (
        temperature if temperature is not None else get_default_temperature()
    )
    target_max_tokens = (
        max_tokens if max_tokens is not None else get_default_max_tokens()
    )
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    msg_objects = normalize_messages(messages)
    request = PlatformModelRequest(
        model=target_model,
        messages=msg_objects,
        temperature=target_temperature,
        max_tokens=target_max_tokens,
        stream=False,
    )
    return invoke_with_request_object(request, client=client)
