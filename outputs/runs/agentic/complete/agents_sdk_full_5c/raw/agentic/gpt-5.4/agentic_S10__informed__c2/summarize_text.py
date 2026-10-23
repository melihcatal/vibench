from __future__ import annotations

from model_client import OpenAIModelClient, build_text_request


def summarize_text(text: str, *, max_tokens: int = 220, model: str = "gpt-4o-mini") -> str:
    client = OpenAIModelClient(model=model)
    request = build_text_request(
        system_prompt="You are a concise summarization assistant. Produce a faithful summary with key points and no hallucinations.",
        user_prompt=f"Summarize the following text in a compact but informative way:\n\n{text}",
        model=model,
        temperature=0.2,
        max_tokens=max_tokens,
    )
    return client.complete(request).content.strip()
