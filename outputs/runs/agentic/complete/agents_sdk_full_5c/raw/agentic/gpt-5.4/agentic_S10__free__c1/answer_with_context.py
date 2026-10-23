from __future__ import annotations

from model_client import choose_model, coalesce_text, get_openai_client
from model_models import ChatMessage, GenerationResult, messages_to_dicts


def answer_with_context(question: str, context: str) -> GenerationResult:
    client = get_openai_client()
    prompt = coalesce_text([
        "Use only the provided context to answer the question.",
        f"Context:\n{context}",
        f"Question:\n{question}",
        "If the answer is not in the context, say that the context does not contain the answer.",
    ])
    response = client.chat.completions.create(
        model=choose_model("qa"),
        messages=messages_to_dicts(
            [
                ChatMessage(role="system", content="You are a careful question-answering assistant."),
                ChatMessage(role="user", content=prompt),
            ]
        ),
        temperature=0.1,
        max_tokens=250,
    )
    choice = response.choices[0]
    return GenerationResult(
        text=choice.message.content or "",
        model=response.model,
        finish_reason=choice.finish_reason,
        raw_response=response.model_dump(),
    )
