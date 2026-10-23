from __future__ import annotations

from model_client import DEFAULT_OPENAI_MODEL, LLMRequest, chat_completion

SYSTEM_PROMPT = "You summarize long text into concise, faithful summaries."


def summarize_text(text: str, model: str = DEFAULT_OPENAI_MODEL) -> str:
    request = LLMRequest(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Summarize the following text:\n{text}"},
        ],
        temperature=0.2,
        max_tokens=300,
    )
    return chat_completion(request).text
