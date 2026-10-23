from __future__ import annotations

from typing import Dict, List, Optional

from model_client import get_platform_client
from model_models import PlatformRequest, PlatformResponse, normalize_messages


def invoke_platform_model(
    prompt: str,
    model_id: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stop: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> PlatformResponse:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    messages = normalize_messages(prompt, system_prompt, conversation_history)

    request = PlatformRequest(
        model_id=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop,
        stream=False,
    )

    response = client.chat_completion(request)
    return response


def invoke_with_tools(
    prompt: str,
    model_id: str = "gpt-4o",
    tools: Optional[List[Dict]] = None,
    tool_choice: Optional[str] = None,
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> PlatformResponse:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    messages = normalize_messages(prompt, system_prompt, conversation_history)

    request = PlatformRequest(
        model_id=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        extra_params={
            "tools": tools or [],
            "tool_choice": tool_choice or "auto",
        }
        if tools
        else {},
    )

    response = client.chat_completion(request)
    return response
