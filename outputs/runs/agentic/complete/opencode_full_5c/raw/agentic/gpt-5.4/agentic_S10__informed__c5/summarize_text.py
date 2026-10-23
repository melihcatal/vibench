from __future__ import annotations

from model_client import DEFAULT_CHAT_MODEL, build_messages, chat_completion_text
from model_models import GenerationConfig, SummarizeRequest


def summarize_text(request: SummarizeRequest, model: str = DEFAULT_CHAT_MODEL) -> str:
    system_prompt = "You are an OpenAI summarization assistant that creates faithful summaries of long passages."
    user_prompt = (
        f"Summarize the following text in a {request.style} style and keep it under "
        f"{request.max_words} words. Preserve the main facts and conclusions.\n\nText:\n{request.text}"
    )
    return chat_completion_text(
        build_messages(system_prompt, user_prompt),
        model=model,
        config=GenerationConfig(temperature=0.2, max_output_tokens=220, top_p=0.9),
    )
