from __future__ import annotations

from model_client import build_generation_config, create_chat_completion, extract_text_and_usage
from model_models import ChatMessage, SummaryResult, trim_text


def summarize_text(text: str, max_summary_tokens: int = 220) -> SummaryResult:
    source_text = trim_text(text, 24000)
    messages = [
        ChatMessage(role="system", content="You are an expert summarizer. Produce a concise, faithful summary with key points and no hallucinations."),
        ChatMessage(role="user", content=f"Summarize the following text in 3-5 sentences:\n\n{source_text}"),
    ]
    response = create_chat_completion(
        messages,
        config=build_generation_config(model="gpt-4o-mini", temperature=0.2, max_tokens=max_summary_tokens),
    )
    parsed = extract_text_and_usage(response)
    return SummaryResult(summary=parsed["text"], model=parsed["model"], usage=parsed["usage"])
