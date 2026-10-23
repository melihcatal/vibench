from __future__ import annotations

from model_client import get_azure_openai_client
from model_models import ModelPrompt, NormalizedGeneration
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: ModelPrompt) -> NormalizedGeneration:
    client = get_azure_openai_client()
    resource = select_platform_resource(task="chat")
    response = client.chat.completions.create(
        model=resource.deployment_name or resource.model_id,
        messages=prompt.to_messages(),
        temperature=prompt.temperature,
        max_tokens=prompt.max_output_tokens,
    )
    message = response.choices[0].message
    return NormalizedGeneration(
        text=message.content or "",
        model=response.model,
        resource_id=resource.deployment_name,
        usage=response.usage.model_dump() if response.usage else {},
        raw=response,
    )
