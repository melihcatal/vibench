from __future__ import annotations

from model_client import choose_model, get_openai_client
from model_models import ChatMessage, GenerationRequest, GenerationResult, messages_to_dicts


def summarize_text(long_text: str) -> GenerationResult:
    client = get_openai_client()
    request = GenerationRequest(
        model=choose_model("summary"),
        messages=[
            ChatMessage(role="system", content="Summarize the input into a concise executive summary with key points."),
            ChatMessage(role="user", content=long_text),
        ],
        temperature=0.2,
        max_output_tokens=300,
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=messages_to_dicts(request.messages),
        temperature=request.temperature,
        max_tokens=request.max_output_tokens,
    )
    choice = response.choices[0]
    return GenerationResult(
        text=choice.message.content or "",
        model=response.model,
        finish_reason=choice.finish_reason,
        raw_response=response.model_dump(),
    )
