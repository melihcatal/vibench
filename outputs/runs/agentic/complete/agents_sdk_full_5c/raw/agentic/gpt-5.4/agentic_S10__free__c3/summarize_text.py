from __future__ import annotations

from model_client import get_openai_client, pick_chat_model
from model_models import ChatRequest, ChatResult, extract_text_from_response, usage_to_dict


def summarize_text(long_text: str, max_words: int = 120) -> ChatResult:
    client = get_openai_client()
    request = ChatRequest(
        system_prompt="You summarize long-form text into concise, accurate summaries with key points preserved.",
        user_prompt=f"Summarize the following text in no more than {max_words} words:\n\n{long_text}",
        model=pick_chat_model("summary"),
        temperature=0.2,
        max_output_tokens=220,
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=request.to_openai_messages(),
        temperature=request.temperature,
        max_tokens=request.max_output_tokens,
    )
    text = extract_text_from_response(response)
    finish_reason = response.choices[0].finish_reason if response.choices else None
    return ChatResult(
        text=text,
        model=request.model,
        usage=usage_to_dict(response),
        finish_reason=finish_reason,
    )
