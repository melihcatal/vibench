"""Invoke a provider-managed model through a deployment-scoped platform client.

Provider: Azure OpenAI Service via openai.
"""

from __future__ import annotations

from model_client import build_client, build_messages, load_config
from model_models import ConversationRequest, ChatMessage, PlatformOutput
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str) -> PlatformOutput:
    resource = select_platform_resource()
    client = build_client()
    request = ConversationRequest(messages=[ChatMessage(role="user", content=prompt)])
    completion = client.chat.completions.create(
        model=resource.deployment,
        messages=build_messages(request),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    text = completion.choices[0].message.content or ""
    return PlatformOutput(
        text=text,
        model=completion.model,
        usage=dict(completion.usage.model_dump() if hasattr(completion.usage, "model_dump") else vars(completion.usage)),
        resource_id=resource.deployment,
        raw=completion,
    )
