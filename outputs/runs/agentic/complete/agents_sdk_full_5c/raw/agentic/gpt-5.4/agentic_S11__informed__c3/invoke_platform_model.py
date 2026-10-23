from __future__ import annotations

from model_client import get_azure_openai_client, load_azure_platform_config, resolve_chat_deployment
from model_models import ModelRequest, ModelResult, ModelChoice, first_text_from_choices, usage_to_dict


def invoke_platform_model(request: ModelRequest) -> ModelResult:
    config = load_azure_platform_config()
    client = get_azure_openai_client(config)
    deployment = resolve_chat_deployment(config)
    response = client.chat.completions.create(
        model=deployment,
        messages=request.to_openai_messages(),
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )
    text = first_text_from_choices(response.choices)
    choices = [
        ModelChoice(
            index=choice.index,
            text=getattr(getattr(choice, "message", None), "content", "") or "",
            finish_reason=getattr(choice, "finish_reason", None),
        )
        for choice in response.choices
    ]
    return ModelResult(
        text=text,
        model=getattr(response, "model", deployment),
        resource_id=deployment,
        usage=usage_to_dict(getattr(response, "usage", None)),
        choices=choices,
        raw=response,
    )
