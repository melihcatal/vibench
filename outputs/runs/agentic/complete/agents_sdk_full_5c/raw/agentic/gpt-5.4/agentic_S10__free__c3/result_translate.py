from __future__ import annotations

from model_client import get_openai_client, pick_chat_model
from model_models import ChatRequest, ChatResult, extract_text_from_response, usage_to_dict


def translate_result(text: str, target_language: str) -> ChatResult:
    client = get_openai_client()
    request = ChatRequest(
        system_prompt="Translate text faithfully while preserving meaning, formatting, and named entities.",
        user_prompt=f"Translate the following text into {target_language}:\n\n{text}",
        model=pick_chat_model("translate"),
        temperature=0.1,
        max_output_tokens=400,
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=request.to_openai_messages(),
        temperature=request.temperature,
        max_tokens=request.max_output_tokens,
    )
    return ChatResult(
        text=extract_text_from_response(response),
        model=request.model,
        usage=usage_to_dict(response),
        finish_reason=response.choices[0].finish_reason if response.choices else None,
    )
