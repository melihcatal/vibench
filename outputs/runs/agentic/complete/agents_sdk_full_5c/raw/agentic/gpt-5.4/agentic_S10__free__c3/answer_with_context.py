from __future__ import annotations

from model_client import get_openai_client, pick_chat_model
from model_models import ChatRequest, ChatResult, extract_text_from_response, usage_to_dict


def answer_with_context(question: str, context: str) -> ChatResult:
    client = get_openai_client()
    request = ChatRequest(
        system_prompt=(
            "Answer using only the provided context. "
            "If the answer is not supported by the context, say you do not know."
        ),
        user_prompt=f"Context:\n{context}\n\nQuestion: {question}",
        model=pick_chat_model("qa"),
        temperature=0.1,
        max_output_tokens=300,
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
