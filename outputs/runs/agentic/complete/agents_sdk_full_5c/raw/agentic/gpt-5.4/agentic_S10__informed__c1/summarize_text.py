from __future__ import annotations

from model_client import HostedModelClient
from model_models import GenerationOptions, build_messages


def summarize_text(text: str, max_summary_tokens: int = 180) -> str:
    client = HostedModelClient()
    model = client.select_model_family("summary")
    messages = build_messages(
        system_prompt="You are a precise summarization assistant. Produce a concise summary with key facts and no speculation.",
        user_prompt=f"Summarize the following text in a clear paragraph and a short bullet list of takeaways.\n\n{text}",
    )
    result = client.chat(
        messages,
        GenerationOptions(model=model, temperature=0.2, max_tokens=max_summary_tokens),
    )
    return result.text
