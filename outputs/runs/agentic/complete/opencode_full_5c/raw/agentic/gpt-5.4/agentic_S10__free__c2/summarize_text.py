from __future__ import annotations

from model_client import get_openai_client, messages_to_dicts, resolve_chat_config
from model_models import TextGenerationResult, normalize_messages, usage_to_dict


def summarize_text(long_text: str, style: str = "concise") -> TextGenerationResult:
    client = get_openai_client()
    config = resolve_chat_config(
        model="gpt-4.1-mini", temperature=0.2, max_output_tokens=400
    )
    messages = normalize_messages(
        system_prompt="You summarize long-form text accurately and preserve key facts.",
        user_prompt=f"Summarize the following text in a {style} style:\n\n{long_text}",
    )
    response = client.responses.create(
        model=config.model,
        input=messages_to_dicts(messages),
        temperature=config.temperature,
        max_output_tokens=config.max_output_tokens,
    )
    return TextGenerationResult(
        provider="openai",
        model=config.model,
        text=response.output_text,
        usage=usage_to_dict(
            input_tokens=getattr(response.usage, "input_tokens", None)
            if getattr(response, "usage", None)
            else None,
            output_tokens=getattr(response.usage, "output_tokens", None)
            if getattr(response, "usage", None)
            else None,
            total_tokens=getattr(response.usage, "total_tokens", None)
            if getattr(response, "usage", None)
            else None,
        ),
    )
