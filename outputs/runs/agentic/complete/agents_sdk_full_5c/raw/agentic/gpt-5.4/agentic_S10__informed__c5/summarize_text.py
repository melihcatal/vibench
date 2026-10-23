from __future__ import annotations

from model_client import complete_text
from model_models import InferenceRequest


def summarize_text(text: str, max_summary_tokens: int = 220, model: str | None = None) -> str:
    request = InferenceRequest(
        system_prompt="You are a concise summarization assistant.",
        user_prompt=(
            "Summarize the following text into a clear executive summary with key points and major conclusions.\n\n"
            f"Text:\n{text}"
        ),
        temperature=0.2,
        max_tokens=max_summary_tokens,
        model=model,
    )
    response = complete_text(request)
    return response.text.strip()
