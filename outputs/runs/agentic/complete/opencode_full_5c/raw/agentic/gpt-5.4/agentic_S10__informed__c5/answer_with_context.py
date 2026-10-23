from __future__ import annotations

from model_client import DEFAULT_CHAT_MODEL, build_messages, chat_completion_text
from model_models import AnswerWithContextRequest, GenerationConfig


def answer_with_context(
    request: AnswerWithContextRequest, model: str = DEFAULT_CHAT_MODEL
) -> str:
    system_prompt = "You are an OpenAI question answering assistant. Answer only from the provided context and say when the context is insufficient."
    user_prompt = (
        f"Context:\n{request.context}\n\nQuestion: {request.question}\n"
        f"Provide a {request.answer_style} answer grounded in the context."
    )
    return chat_completion_text(
        build_messages(system_prompt, user_prompt),
        model=model,
        config=GenerationConfig(temperature=0.1, max_output_tokens=260, top_p=0.9),
    )
